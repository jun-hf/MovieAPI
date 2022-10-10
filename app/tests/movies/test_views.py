import json

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