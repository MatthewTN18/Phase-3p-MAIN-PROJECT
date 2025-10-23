"""
Cinema Kiosk CLI Application: main menu and navigation
"""

from src.models import SessionLocal
from src.services.movie_service import MovieService
from src.services.booking_service import BookingService

class CinemaKiosk:
    def __init__(self):
        self.session = SessionLocal()
        self.movie_service = MovieService(self.session)
        self.booking_service = BookingService(self.session)
        self.current_customer = None
        
    def display_header(self):
        print("\n" + "=" * 50)
        print("           CINEMA KIOSK")
        print("=" * 50)
    
    def display_main_menu(self):
        print("\nMAIN MENU:")
        print("1. Browse Movies & Showtimes")
        print("2. Make a Reservation")
        print("3. View My Tickets")
        print("4. Exit")
        print("-" * 30)
    
    def display_movies(self, movies):
        """Display movies in a formatted list"""
        if not movies:
            print("No movies currently showing.")
            return
        
        print(f"\nNOW SHOWING ({len(movies)} movies):")
        for i, movie in enumerate(movies, 1):
            print(f"\n{i}. {movie.title}")
            print(f"   Genre: {movie.genre}")
            print(f"   Duration: {movie.duration} minutes")
            
            showtimes = self.movie_service.get_showtimes_for_movie(movie.id)
            if showtimes:
                print("   Showtimes:")
                for st in showtimes:
                    print(f"     - {st.show_date} at {st.show_time} ({st.available_seats} seats available)")
            else:
                print("   No upcoming showtimes")
    
    def display_seat_map(self, seats):
        if not seats:
            print("No seats available.")
            return
        
        rows = {}
        for seat in seats:
            if seat.row_letter not in rows:
                rows[seat.row_letter] = []
            rows[seat.row_letter].append(seat)
        
        sorted_rows = sorted(rows.items())
        
        print("\n" + " " * 10 + "SCREEN")
        print(" " * 8 + "─" * 20)
        print()
        
        for row_letter, row_seats in sorted_rows:
            print(f"{row_letter} ", end="")
            for seat in sorted(row_seats, key=lambda s: s.seat_number):
                symbol = "[ ]" if seat.is_available_for_showtime else "[X]"
                print(f"{symbol} ", end="")
            print()
        
        print("  ", end="")
        max_seats = max(len(seats) for seats in rows.values())
        for i in range(1, max_seats + 1):
            print(f" {i}  ", end="")
        print()
        
        print("\nKey map: [ ] = Available, [X] = Taken")
    
    def handle_snack_selection(self):
        """Snack selection """
        snacks = self.booking_service.get_available_snacks()
        
        if not snacks:
            print("No snacks available at this time.")
            return {}, 0
        
        print("\n--- SNACK MENU ---")
        for i, snack in enumerate(snacks, 1):
            print(f"{i}. {snack.name} - ${snack.price:.2f}")
        
        print("\nSelect snacks (e.g., '1 2' for items 1 and 2, or press Enter to skip):")
        choice = input("Your choice: ").strip()
        
        if not choice:
            return {}, 0
        
        snack_orders = {}
        total = 0
        
        try:
            selections = choice.split()
            for selection in selections:
                snack_index = int(selection) - 1
                if 0 <= snack_index < len(snacks):
                    snack = snacks[snack_index]
                    
                    print(f"How many {snack.name}? (Available: {snack.stock_quantity}): ")
                    quantity = int(input("Quantity: ").strip())
                    
                    if 1 <= quantity <= snack.stock_quantity:
                        snack_orders[snack.id] = quantity
                        total += snack.price * quantity
                        print(f"Added {quantity}x {snack.name}")
                    else:
                        print(f"Invalid quantity. Available: {snack.stock_quantity}")
                else:
                    print(f"Invalid snack number: {selection}")
        
        except ValueError:
            print("Invalid input. No snacks added.")
        
        return snack_orders, total
    
    def handle_movie_browsing(self):
        print("\n--- Browse Movies ---")
        
        movies = self.movie_service.get_now_showing()
        self.display_movies(movies)
        
        if movies:
            print("\nSelect a movie number for more options or 'back' to return.")
            choice = input("Your choice: ").strip().lower()
            
            if choice != 'back':
                try:
                    movie_index = int(choice) - 1
                    if 0 <= movie_index < len(movies):
                        self.handle_movie_selection(movies[movie_index])
                    else:
                        print("Invalid movie selection.")
                except ValueError:
                    print("Please enter a valid number or 'back'.")
        
        input("\nPress Enter to continue...")
    
    def handle_movie_selection(self, movie):
        print(f"\n--- {movie.title} ---")
        
        showtimes = self.movie_service.get_showtimes_for_movie(movie.id)
        if not showtimes:
            print("No showtimes available for this movie.")
            return
        
        print("Available showtimes:")
        for i, st in enumerate(showtimes, 1):
            print(f"{i}. {st.show_date} at {st.show_time} ({st.available_seats} seats available)")
        
        print("\nSelect a showtime or 'back' to return.")
        choice = input("Your choice: ").strip().lower()
        
        if choice != 'back':
            try:
                showtime_index = int(choice) - 1
                if 0 <= showtime_index < len(showtimes):
                    self.handle_showtime_selection(showtimes[showtime_index])
                else:
                    print("Invalid showtime selection.")
            except ValueError:
                print("Please enter a valid number or 'back'.")
    
    def handle_showtime_selection(self, showtime):
        print(f"\n--- {showtime.movie.title} at {showtime.show_time} ---")
        
        seats = self.booking_service.get_available_seats(showtime.id)
        self.display_seat_map(seats)
        
        if seats:
            print("\nSelect seats (e.g., 'A1 A2 B3' or 'back' to return):")
            choice = input("Your choice: ").strip().lower()
            
            if choice != 'back':
                selected_seats = self.parse_seat_selection(choice, seats)
                if selected_seats:
                    self.handle_seat_selection(showtime, selected_seats)
                else:
                    print("Invalid seat selection.")
    
    def parse_seat_selection(self, input_str, available_seats):
        try:
            selections = input_str.upper().split()
            selected_seats = []
            
            for selection in selections:
                row_letter = selection[0]
                seat_number = int(selection[1:])
                
                matching_seat = None
                for seat in available_seats:
                    if (seat.row_letter == row_letter and 
                        seat.seat_number == seat_number and 
                        seat.is_available_for_showtime):
                        matching_seat = seat
                        break
                
                if matching_seat:
                    selected_seats.append(matching_seat)
                else:
                    print(f"Seat {selection} is not available or invalid.")
                    return None
            
            return selected_seats
            
        except (ValueError, IndexError):
            print("Invalid seat format. Use format like 'A1 A2 B3'")
            return None
    
    def handle_seat_selection(self, showtime, selected_seats):
        print(f"\nSelected {len(selected_seats)} seats:")
        for seat in selected_seats:
            print(f"  - {seat.row_letter}{seat.seat_number}")
        
        ticket_total = showtime.base_price * len(selected_seats)
        print(f"Ticket Total: ${ticket_total:.2f}")
        
        # Snack selection
        snack_orders, snack_total = self.handle_snack_selection()
        grand_total = ticket_total + snack_total
        
        if snack_total > 0:
            print(f"Snack Total: ${snack_total:.2f}")
        
        print(f"Grand Total: ${grand_total:.2f}")
        
        while True:
            print("\nEnter your email for tickets:")
            customer_email = input("Email: ").strip()
            if customer_email: 
                break
            else:
                print("Email is required.")

        print(f"\nConfirm booking for ${grand_total:.2f}? (yes/no)")
        confirmation = input("Confirm: ").strip().lower()
        
        if confirmation in ['yes', 'y']:
            seat_ids = [seat.id for seat in selected_seats]
            reservation, tickets, snack_details = self.booking_service.create_reservation(
                showtime.id, seat_ids, customer_email, snack_orders
            )
            
            if reservation and tickets:
                self.display_booking_confirmation(reservation, tickets, snack_details, snack_total)
            else:
                print("Booking failed. Please try again.")
        else:
            print("Booking cancelled.")
        
        input("\nPress Enter to continue...")
    
    def display_booking_confirmation(self, reservation, tickets, snack_details, snack_total):
        print("\n" + "=" * 40)
        print("      BOOKING CONFIRMED!")
        print("=" * 40)
        
        showtime = reservation.showtime
        movie = showtime.movie
        
        print(f"\nMovie: {movie.title}")
        print(f"Showtime: {showtime.show_date} at {showtime.show_time}")
        print(f"Tickets: ${showtime.base_price * len(tickets):.2f}")
        
        if snack_total > 0:
            print(f"Snacks: ${snack_total:.2f}")
            print("Snack Order:")
            for snack in snack_details:
                print(f"  - {snack}")
        
        print(f"Total Paid: ${reservation.total_amount:.2f}")
        
        print(f"\nYour Tickets ({len(tickets)}):")
        for ticket in tickets:
            seat = ticket.seat
            print(f"  - {ticket.ticket_number} (Seat {seat.row_letter}{seat.seat_number})")
        
        if reservation.customer:
            print(f"\nTickets sent to: {reservation.customer.email}")
        
        print("\nThank you for your purchase! Enjoy the movie!")
    
    def handle_view_tickets(self):
        """View tickets by email lookup"""
        print("\n--- View My Tickets ---")
        
        print("Enter your email to view tickets:")
        customer_email = input("Email: ").strip()
        
        if not customer_email:
            print("Email is required.")
            input("\nPress Enter to continue...")
            return
        
        try:
            from src.models import Customer, Reservation, Ticket, Showtime, Movie
            
            # Find customer by email
            customer = self.session.query(Customer).filter(Customer.email == customer_email).first()
            
            if not customer:
                print(f"No tickets found for email: {customer_email}")
                input("\nPress Enter to continue...")
                return
            
            # Get all reservations for this customer
            reservations = (self.session.query(Reservation)
                           .filter(Reservation.customer_id == customer.id)
                           .filter(Reservation.status == 'confirmed')
                           .order_by(Reservation.created_at.desc())
                           .all())
            
            if not reservations:
                print(f"No tickets found for email: {customer_email}")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nFound {len(reservations)} booking(s) for {customer_email}:")
            
            for i, reservation in enumerate(reservations, 1):
                showtime = reservation.showtime
                movie = showtime.movie
                
                print(f"\n{i}. {movie.title}")
                print(f"   Showtime: {showtime.show_date} at {showtime.show_time}")
                print(f"   Booked on: {reservation.created_at.strftime('%Y-%m-%d %H:%M')}")
                print(f"   Total Paid: ${reservation.total_amount:.2f}")
                
                # Get tickets for this reservation
                tickets = (self.session.query(Ticket)
                          .filter(Ticket.reservation_id == reservation.id)
                          .all())
                
                print("   Tickets:")
                for ticket in tickets:
                    seat = ticket.seat
                    print(f"     - {ticket.ticket_number} (Seat {seat.row_letter}{seat.seat_number})")
                
                # Get snack orders for this reservation
                from src.models import SnackOrder, Snack
                snack_orders = (self.session.query(SnackOrder)
                               .join(Snack)
                               .filter(SnackOrder.reservation_id == reservation.id)
                               .all())
                
                if snack_orders:
                    print("   Snacks:")
                    for order in snack_orders:
                        print(f"     - {order.quantity}x {order.snack.name} (${order.subtotal:.2f})")
            
            print(f"\nTotal bookings: {len(reservations)}")
            
        except Exception as e:
            print(f"Error retrieving tickets: {e}")
        
        input("\nPress Enter to continue...")
    
    def handle_reservation(self):
        print("\n--- Make Reservation ---")
        self.handle_movie_browsing()
    
    def run(self):
        try:
            while True:
                self.display_header()
                self.display_main_menu()
                
                choice = input("Select an option (1-4): ").strip()
                
                if choice == "1":
                    self.handle_movie_browsing()
                elif choice == "2":
                    self.handle_reservation()
                elif choice == "3":
                    self.handle_view_tickets()
                elif choice == "4":
                    print("\nThank you for using Cinema Kiosk!")
                    break
                else:
                    print("\nInvalid option. Please try again.")
                    input("Press Enter to continue...")
                    
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            self.session.close()