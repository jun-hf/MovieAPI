import pytest 

from movies.models import Movie

@pytest.mark.django_db
def test_movie_model():
    movie = Movie(title="Happy feet", genre="comedy", year="1987")
    movie.save() 

    assert movie.title == "Happy feet"
    assert movie.genre == "comedy"
    assert movie.year == "1987"
    assert movie.created_date 
    assert movie.updated_date 
    assert str(movie) == movie.title

    