"""
Handling movie-related services
"""

from src.models import Movie, Showtime, Screen
from datetime import datetime, timedelta

class MovieService:
    def __init__(self, session):
        self.session = session
    
    def get_now_showing(self, days=7):
        """Get movies showing in the next few days - INCLUDING TODAY"""
        try:
            # Starting from today 
            today = datetime.now().date()
            end_date = today + timedelta(days=days)
            
            movies = (self.session.query(Movie)
                     .join(Showtime)
                     .filter(Showtime.show_date >= today.strftime('%Y-%m-%d'))
                     .filter(Showtime.show_date <= end_date.strftime('%Y-%m-%d'))
                     .filter(Movie.is_active == True)
                     .distinct()
                     .all())
            
            return movies
            
        except Exception as e:
            print(f"Error getting movies: {e}")
            return []
    
    def get_showtimes_for_movie(self, movie_id, date=None):
        """Get showtimes for a specific movie - INCLUDING TODAY"""
        try:
            query = (self.session.query(Showtime)
                     .join(Screen)
                     .filter(Showtime.movie_id == movie_id))
            
            # Always include today and future
            today = datetime.now().date().strftime('%Y-%m-%d')
            query = query.filter(Showtime.show_date >= today)
            
            if date:
                # filter by specific date
                query = query.filter(Showtime.show_date == date)
            
            # Order by date and time
            showtimes = (query.order_by(Showtime.show_date, Showtime.show_time)
                         .all())
            
            return showtimes
            
        except Exception as e:
            print(f"Error getting showtimes: {e}")
            return []
    
    def get_showtimes_by_date(self, date=None):
        """Get all showtimes for a specific date - defaults to TODAY"""
        try:
            if not date:
                date = datetime.now().date().strftime('%Y-%m-%d')
            
            showtimes = (self.session.query(Showtime)
                         .join(Movie)
                         .join(Screen)
                         .filter(Showtime.show_date == date)
                         .order_by(Showtime.show_time)
                         .all())
            
            return showtimes
            
        except Exception as e:
            print(f"Error getting showtimes by date: {e}")
            return []
    
    def get_all_upcoming_showtimes(self):
        """Get ALL showtimes from today onward (for debugging)"""
        try:
            today = datetime.now().date().strftime('%Y-%m-%d')
            
            showtimes = (self.session.query(Showtime)
                         .join(Movie)
                         .join(Screen)
                         .filter(Showtime.show_date >= today)
                         .order_by(Showtime.show_date, Showtime.show_time)
                         .all())
            
            return showtimes
            
        except Exception as e:
            print(f"Error getting upcoming showtimes: {e}")
            return []