"""
Booking service handling 
"""

from src.models import Seat, Reservation, ReservationSeat

class BookingService:
    def __init__(self, session):
        self.session = session
    
    def get_available_seats(self, showtime_id):
        """Get available seats for a showtime"""
        pass  
    
    def create_reservation(self, showtime_id, seat_ids, customer_email=None):
        """Create a new reservation"""
        pass  