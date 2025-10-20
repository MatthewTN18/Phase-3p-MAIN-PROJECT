from .orm_db import Base, engine, SessionLocal, get_db, create_tables
from .movies import Movie
from .screens import Screen
from .showtimes import Showtime
from .seats import Seat
from .customers import Customer
from .reservations import Reservation
from .reservation_seats import ReservationSeat
from .snacks import Snack
from .snack_orders import SnackOrder
from .tickets import Ticket


from sqlalchemy.orm import relationship

# Movie relationships
Movie.showtimes = relationship("Showtime", back_populates="movie")

# Screen relationships
Screen.showtimes = relationship("Showtime", back_populates="screen")
Screen.seats = relationship("Seat", back_populates="screen")

# Showtime relationships
Showtime.movie = relationship("Movie", back_populates="showtimes")
Showtime.screen = relationship("Screen", back_populates="showtimes")
Showtime.reservations = relationship("Reservation", back_populates="showtime")

# Seat relationships
Seat.screen = relationship("Screen", back_populates="seats")
Seat.reservation_seats = relationship("ReservationSeat", back_populates="seat")
Seat.tickets = relationship("Ticket", back_populates="seat")

# Customer relationships
Customer.reservations = relationship("Reservation", back_populates="customer")

# Reservation relationships
Reservation.showtime = relationship("Showtime", back_populates="reservations")
Reservation.customer = relationship("Customer", back_populates="reservations")
Reservation.reservation_seats = relationship("ReservationSeat", back_populates="reservation")
Reservation.snack_orders = relationship("SnackOrder", back_populates="reservation")
Reservation.tickets = relationship("Ticket", back_populates="reservation")

# ReservationSeat relationships
ReservationSeat.reservation = relationship("Reservation", back_populates="reservation_seats")
ReservationSeat.seat = relationship("Seat", back_populates="reservation_seats")

# Snack relationships
Snack.snack_orders = relationship("SnackOrder", back_populates="snack")

# SnackOrder relationships
SnackOrder.reservation = relationship("Reservation", back_populates="snack_orders")
SnackOrder.snack = relationship("Snack", back_populates="snack_orders")

# Ticket relationships
Ticket.reservation = relationship("Reservation", back_populates="tickets")
Ticket.seat = relationship("Seat", back_populates="tickets")

__all__ = [
    'Base', 'engine', 'SessionLocal', 'get_db', 'create_tables',
    'Movie', 'Screen', 'Showtime', 'Seat', 'Customer', 'Reservation',
    'ReservationSeat', 'Snack', 'SnackOrder', 'Ticket'
]