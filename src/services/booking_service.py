"""
Booking service handling reservation operations
"""

from src.models import Seat, Reservation, ReservationSeat, Showtime
from sqlalchemy.orm import joinedload

class BookingService:
    def __init__(self, session):
        self.session = session
    
    def get_available_seats(self, showtime_id):
        """Get available seats for a specific showtime"""
        try:
            
            showtime = self.session.query(Showtime).filter(Showtime.id == showtime_id).first()
            if not showtime:
                return []
            
            # Get all seats for this screen
            all_seats = (self.session.query(Seat)
                        .filter(Seat.screen_id == showtime.screen_id)
                        .order_by(Seat.row_letter, Seat.seat_number)
                        .all())
            
            # Get seats that are already reserved 
            reserved_seat_ids = (
                self.session.query(ReservationSeat.seat_id)
                .join(Reservation)
                .filter(Reservation.showtime_id == showtime_id)
                .filter(Reservation.status == 'confirmed')
                .all()
            )
            reserved_seat_ids = [seat_id for (seat_id,) in reserved_seat_ids]
            
            # Mark availability
            for seat in all_seats:
                seat.is_available_for_showtime = seat.id not in reserved_seat_ids
            
            return all_seats
            
        except Exception as e:
            print(f"Error getting available seats: {e}")
            return []
    
    def create_reservation(self, showtime_id, seat_ids, customer_email=None):
        """Create a new reservation"""
        try:
            
            showtime = self.session.query(Showtime).filter(Showtime.id == showtime_id).first()
            if not showtime:
                return None
            
            # Create customer record 
            customer_id = None
            if customer_email:
                from src.models import Customer
                customer = self.session.query(Customer).filter(Customer.email == customer_email).first()
                if not customer:
                    customer = Customer(email=customer_email)
                    self.session.add(customer)
                    self.session.flush()
                customer_id = customer.id
            
            # Calculate total 
            total_amount = showtime.base_price * len(seat_ids)
            
            # Create reservation
            reservation = Reservation(
                showtime_id=showtime_id,
                customer_id=customer_id,
                total_amount=total_amount,
                status='confirmed'
            )
            self.session.add(reservation)
            self.session.flush()  # Get the reservation ID
            
            # Create reservation_seat records
            for seat_id in seat_ids:
                reservation_seat = ReservationSeat(
                    reservation_id=reservation.id,
                    seat_id=seat_id
                )
                self.session.add(reservation_seat)
            
            # Update available seats 
            showtime.available_seats -= len(seat_ids)
            
            self.session.commit()
            return reservation
            
        except Exception as e:
            self.session.rollback()
            print(f"Error creating reservation: {e}")
            return None
    
    def are_seats_available(self, showtime_id, seat_ids):
        """Check if specific seats are available for a showtime"""
        try:
            available_seats = self.get_available_seats(showtime_id)
            available_seat_ids = [seat.id for seat in available_seats if seat.is_available_for_showtime]
            
            return all(seat_id in available_seat_ids for seat_id in seat_ids)
            
        except Exception as e:
            print(f"Error checking seat availability: {e}")
            return False