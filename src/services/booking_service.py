"""
Booking service handling reservation operations
"""

from src.models import Seat, Reservation, ReservationSeat, Showtime, Ticket, Snack, SnackOrder
from sqlalchemy.orm import joinedload
import random
import string

class BookingService:
    def __init__(self, session):
        self.session = session
    
    def generate_ticket_number(self):
        """Generate unique ticket number: CINYYYYMMDD-RANDOM"""
        from datetime import datetime
        date_str = datetime.now().strftime("%Y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"CIN{date_str}-{random_str}"
    
    def get_available_seats(self, showtime_id):
        """Get available seats for a specific showtime"""
        try:
            showtime = self.session.query(Showtime).filter(Showtime.id == showtime_id).first()
            if not showtime:
                return []
            
            all_seats = (self.session.query(Seat)
                        .filter(Seat.screen_id == showtime.screen_id)
                        .order_by(Seat.row_letter, Seat.seat_number)
                        .all())
            
            reserved_seat_ids = (
                self.session.query(ReservationSeat.seat_id)
                .join(Reservation)
                .filter(Reservation.showtime_id == showtime_id)
                .filter(Reservation.status == 'confirmed')
                .all()
            )
            reserved_seat_ids = [seat_id for (seat_id,) in reserved_seat_ids]
            
            for seat in all_seats:
                seat.is_available_for_showtime = seat.id not in reserved_seat_ids
            
            return all_seats
            
        except Exception as e:
            print(f"Error getting available seats: {e}")
            return []
    
    def get_available_snacks(self):
        """Get all available snacks"""
        try:
            snacks = (self.session.query(Snack)
                     .filter(Snack.is_available == True)
                     .filter(Snack.stock_quantity > 0)
                     .order_by(Snack.name)
                     .all())
            return snacks
        except Exception as e:
            print(f"Error getting snacks: {e}")
            return []
    
    def create_reservation(self, showtime_id, seat_ids, customer_email=None, snack_orders=None):
        """Create a new reservation with tickets and optional snacks"""
        try:
            if snack_orders is None:
                snack_orders = {}
                
            showtime = self.session.query(Showtime).filter(Showtime.id == showtime_id).first()
            if not showtime:
                return None, [], "Showtime not found"
            
            customer_id = None
            if customer_email:
                from src.models import Customer
                customer = self.session.query(Customer).filter(Customer.email == customer_email).first()
                if not customer:
                    customer = Customer(email=customer_email)
                    self.session.add(customer)
                    self.session.flush()
                customer_id = customer.id
            
            total_amount = showtime.base_price * len(seat_ids)
            
            reservation = Reservation(
                showtime_id=showtime_id,
                customer_id=customer_id,
                total_amount=total_amount,
                status='confirmed'
            )
            self.session.add(reservation)
            self.session.flush()
            
            tickets = []
            for seat_id in seat_ids:
                reservation_seat = ReservationSeat(
                    reservation_id=reservation.id,
                    seat_id=seat_id
                )
                self.session.add(reservation_seat)
                
                ticket = Ticket(
                    reservation_id=reservation.id,
                    seat_id=seat_id,
                    ticket_number=self.generate_ticket_number(),
                    status='active'
                )
                self.session.add(ticket)
                tickets.append(ticket)
            
            snack_total = 0
            snack_details = []
            
            for snack_id, quantity in snack_orders.items():
                snack = self.session.query(Snack).filter(Snack.id == snack_id).first()
                if snack and snack.stock_quantity >= quantity:
                    subtotal = snack.price * quantity
                    snack_order = SnackOrder(
                        reservation_id=reservation.id,
                        snack_id=snack_id,
                        quantity=quantity,
                        unit_price=snack.price,
                        subtotal=subtotal
                    )
                    self.session.add(snack_order)
                    snack.stock_quantity -= quantity
                    snack_total += subtotal
                    snack_details.append(f"{quantity}x {snack.name}")
            
            total_amount += snack_total
            reservation.total_amount = total_amount
            
            showtime.available_seats -= len(seat_ids)
            
            self.session.commit()
            return reservation, tickets, snack_details
            
        except Exception as e:
            self.session.rollback()
            print(f"Error creating reservation: {e}")
            return None, [], f"Booking failed: {e}"
    
    def are_seats_available(self, showtime_id, seat_ids):
        """Check if specific seats are available for a showtime"""
        try:
            available_seats = self.get_available_seats(showtime_id)
            available_seat_ids = [seat.id for seat in available_seats if seat.is_available_for_showtime]
            
            return all(seat_id in available_seat_ids for seat_id in seat_ids)
            
        except Exception as e:
            print(f"Error checking seat availability: {e}")
            return False