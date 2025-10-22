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
    
    def handle_movie_browsing(self):
        print("\n--- Browse Movies ---")
        
        # Get movies from database
        movies = self.movie_service.get_now_showing()
        
        # Display movies
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
        print("Movie selection feature coming soon!")
        # TODO: Implement seat selection and booking flow
    
    def handle_reservation(self):
        print("\n--- Make Reservation ---")
        pass
    
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