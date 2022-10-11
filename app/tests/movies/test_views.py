import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "Happy Feet!!",
            "genre": "comedy",
            "year": "2001",
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "Happy Feet!!"

    movies = Movie.objects.all()
    assert len(movies) == 1

@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        "/api/movies/",
        {
            "title": "Notebook",
            "genre": "Drama",
        },
        content_type="application/json"
    )
    assert resp.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0

@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="Trumen", genre="comedy", year="2000")
    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Trumen"


def test_get_single_movie_incorrect_id(client):
    resp = client.get(f"/api/movies/foo/")
    assert resp.status_code == 404

@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="Big foot", genre="comedy", year="1998")
    movie_two = add_movie("No", "thriller", "2007")
    resp = client.get("/api/movies/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == movie_one.title
    assert resp.data[1]["title"] == movie_two.title

@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="Happi", genre="comedy", year="2021")

    resp = client.get(f"/api/movies/{movie.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Happi"

    resp_two = client.delete(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 204

    resp_three = client.get("/api/movies/")
    assert resp_three.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    resp = client.delete(f"/api/movies/32/")
    assert resp.status_code == 404

@pytest.mark.django_db 
def test_update_movie(client, add_movie):
    movie = add_movie(title="Happy feet", genre="comedy", year="2010")

    resp = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "Happy feet", "genre": "comedy", "year": "2011"},
        content_type="application/json"
    )

    assert resp.status_code == 200
    assert resp.data["title"] == "Happy feet"
    assert resp.data["year"] == "2011"

    resp_two = client.get(f"/api/movies/{movie.id}/")
    assert resp_two.status_code == 200
    assert resp_two.data["title"] == "Happy feet"
    assert resp.data["year"] == "2011"

@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    resp = client.put(f"/api/movies/99/")
    assert resp.status_code == 404

@pytest.mark.django_db
def test_update_movie_invalid_json(client, add_movie):
    movie = add_movie(title="Keef", genre="comedy", year="2011")
    resp = client.put(f"/api/movies/{movie.id}/", {}, content_type="application/json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_update_movie_invalid_json_keys(client, add_movie):
    movie = add_movie(title="Mod", genre="comedy", year="2009")

    resp = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "Mod", "genre": "comedy"},
        content_type="application/json",
    )
    assert resp.status_code == 400