from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    release_year: int
    director: str
    genre: str
    wiki_page: str
    image_url: str
    imdb_id: str
