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
        # application header
        print("\n" + "=" * 50)
        print("           CINEMA KIOSK")
        print("=" * 50)
    
    def display_main_menu(self):
        # display menu options
        print("\nMAIN MENU:")
        print("1. Browse Movies & Showtimes")
        print("2. Make a Reservation")
        print("3. View My Tickets")
        print("4. Exit")
        print("-" * 30)
    
    def handle_movie_browsing(self):
        
        print("\n--- Browse Movies ---")
        pass  # Implement movie browsing
    
    def handle_reservation(self):
        
        print("\n--- Make Reservation ---")
        pass  # Implement reservation 
    
    def handle_view_tickets(self):
        
        print("\n--- My Tickets ---")
        pass  # Implement ticket viewing
    
    def run(self):
        """Main application loop"""
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