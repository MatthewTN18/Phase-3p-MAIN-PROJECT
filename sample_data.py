from src.models import SessionLocal
from src.models import Movie, Screen, Showtime, Seat, Snack
from datetime import datetime, timedelta

def create_basic_sample_data():
    session = SessionLocal()
    
    try:
        print("Clearing existing sample data...")
        
        session.query(Seat).delete()
        session.query(Showtime).delete()
        session.query(Screen).delete()
        session.query(Snack).delete()
        session.query(Movie).delete()
        session.commit()
        
        print("Creating basic sample data...")
        
        # create movies
        movies = [
            Movie(title="Oppenheimer", genre="Biography", duration=180),
            Movie(title="It", genre="Horror", duration=135),
            Movie(title="The Conjuring", genre="Horror", duration=185),
            Movie(title="Batman", genre="Action", duration=160),
            Movie(title="Beekeeper", genre="Thriller", duration=105), 
            Movie(title="Hit Man", genre="Comedy", duration=115),
            Movie(title="A Minecraft Movie", genre="Adventure", duration=101)
        ]
        session.add_all(movies)
        session.flush()
        print(f"Created {len(movies)} movies")
        
        # create 1 screen
        screens = [
            Screen(number=1, capacity=50, screen_type="Standard")
        ]
        session.add_all(screens)
        session.flush()
        print("Created 1 screen")
        
        # Create 50 seats for the screen
        seats = []
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for row in rows:
            for seat_num in range(1, 6):
                seats.append(Seat(
                    screen_id=screens[0].id,
                    row_letter=row,
                    seat_number=seat_num,
                    seat_type="standard",
                    is_available=True
                ))
        session.add_all(seats)
        session.flush()
        print("Created 50 seats")
        
        # create showtimes 
        showtimes = []
        today = datetime.now().strftime("%Y-%-m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        
        showtimes.append(Showtime(
            movie_id=movies[0].id,  # Oppenheimer
            screen_id=screens[0].id,
            show_time="14:30",
            show_date=today,  
            base_price=12.00,
            available_seats=50
        ))
        
        showtimes.append(Showtime(
            movie_id=movies[1].id,  # It
            screen_id=screens[0].id,
            show_time="19:00", 
            show_date=today,  
            base_price=12.00,
            available_seats=50
        ))
        
        
        showtimes.append(Showtime(
            movie_id=movies[2].id,  # The Conjuring
            screen_id=screens[0].id,
            show_time="16:00",
            show_date=tomorrow,  
            base_price=12.00,
            available_seats=50
        ))
        
        showtimes.append(Showtime(
            movie_id=movies[3].id,  # Batman
            screen_id=screens[0].id,
            show_time="20:30",
            show_date=tomorrow,  
            base_price=12.00,
            available_seats=50
        ))
        
        session.add_all(showtimes)
        session.flush()
        print(f"Created {len(showtimes)} showtimes")
        
        # 3 basic snacks
        snacks = [
            Snack(name="Large Popcorn", category="popcorn", price=8.50, stock_quantity=50),
            Snack(name="Medium Soda", category="drinks", price=4.00, stock_quantity=100),
            Snack(name="Chocolate Candy", category="candy", price=4.50, stock_quantity=75)
        ]
        session.add_all(snacks)
        print("Created 3 snacks")
        
        session.commit()
        
        # Print summary
        print("\nBasic sample data created successfully!")
        print(f"Movies: {len(movies)} total")
        print(f"Showtimes today: 2 ({movies[0].title} at 14:30, {movies[1].title} at 19:00)")
        print(f"Showtimes tomorrow: 2 ({movies[2].title} at 16:00, {movies[3].title} at 20:30)")
        
    except Exception as e:
        session.rollback()
        print(f"Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    create_basic_sample_data()