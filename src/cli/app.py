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
            
            # Get showtimes for this movie
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
        
        # Group seats by row
        rows = {}
        for seat in seats:
            if seat.row_letter not in rows:
                rows[seat.row_letter] = []
            rows[seat.row_letter].append(seat)
        
        # Sort rows alphabetically
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
        
        # Display seat numbers
        print("  ", end="")
        max_seats = max(len(seats) for seats in rows.values())
        for i in range(1, max_seats + 1):
            print(f" {i}  ", end="")
        print()
        
        print("\nKey map: [ ] = Available, [X] = Taken")
    
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
        """Handle when a user selects a specific movie"""
        print(f"\n--- {movie.title} ---")
        
        # Get showtimes for this movie
        showtimes = self.movie_service.get_showtimes_for_movie(movie.id)
        if not showtimes:
            print("No showtimes available for this movie.")
            return
        
        # Display showtimes
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
        """Handle when a user selects a specific showtime"""
        print(f"\n--- {showtime.movie.title} at {showtime.show_time} ---")
        
        # Get available seats
        seats = self.booking_service.get_available_seats(showtime.id)
        
        # Display seat map
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
        """Parse seat selection input like 'A1 A2 B3'"""
        try:
            selections = input_str.upper().split()
            selected_seats = []
            
            for selection in selections:
                # Parse format e.g "A1", "B5"
                row_letter = selection[0]
                seat_number = int(selection[1:])
                
                # Find matching seat
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
        """Complete booking process with confirmation and ticket generation"""
        print(f"\nSelected {len(selected_seats)} seats:")
        for seat in selected_seats:
            print(f"  - {seat.row_letter}{seat.seat_number}")
        
        total_price = showtime.base_price * len(selected_seats)
        print(f"Total: ${total_price:.2f}")
        
        # Get customer email
        while True:
            print("\nEnter your email for tickets:")
            customer_email = input("Email: ").strip()

            if customer_email: 
                break
            else:
                print("Email is required. Please enter your email.")


        # Confirm booking
        print(f"\nConfirm booking for ${total_price:.2f}? (yes/no)")
        confirmation = input("Confirm: ").strip().lower()
        
        if confirmation in ['yes', 'y']:
            # Create reservation
            seat_ids = [seat.id for seat in selected_seats]
            reservation, tickets = self.booking_service.create_reservation(
                showtime.id, seat_ids, customer_email
            )
            
            if reservation and tickets:
                self.display_booking_confirmation(reservation, tickets)
            else:
                print("Booking failed. Please try again.")
        else:
            print("Booking cancelled.")
        
        input("\nPress Enter to continue...")
    
    def display_booking_confirmation(self, reservation, tickets):
        """Display booking confirmation with ticket details"""
        print("\n" + "=" * 40)
        print("      BOOKING CONFIRMED!")
        print("=" * 40)
        
        # Get showtime details
        showtime = reservation.showtime
        movie = showtime.movie
        
        print(f"\nMovie: {movie.title}")
        print(f"Showtime: {showtime.show_date} at {showtime.show_time}")
        print(f"Total Paid: ${reservation.total_amount:.2f}")
        
        print(f"\nYour Tickets ({len(tickets)}):")
        for ticket in tickets:
            seat = ticket.seat
            print(f"  - {ticket.ticket_number} (Seat {seat.row_letter}{seat.seat_number})")
        
        if reservation.customer:
            print(f"\nTickets sent to: {reservation.customer.email}")
        
        print("\nThank you for your purchase! Enjoy the movie! ")
    
    def handle_reservation(self):
        print("\n--- Make Reservation ---")
        self.handle_movie_browsing()
    
    def handle_view_tickets(self):
        print("\n--- My Tickets ---")
        pass
    
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