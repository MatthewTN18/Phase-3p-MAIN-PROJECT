"""
Handling movie-related services
"""

from src.models import Movie, Showtime

class MovieService:
    def __init__(self, session):
        self.session = session
    
    def get_now_showing(self, days=7):
        """Get movies showing in the next few days"""
        pass  
    
    def get_showtimes_for_movie(self, movie_id, date=None):
        """Get showtimes for a specific movie"""
        pass  