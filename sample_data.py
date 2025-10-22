from src.models import SessionLocal
from src.models import Movie, Screen, Showtime, Seat, Snack

def create_basic_sample_data():
    session = SessionLocal()
    
    try:
        print("Clearing existing sample data...")
        # Clear data 
        session.query(Snack).delete()
        session.query(Seat).delete()
        session.query(Showtime).delete()
        session.query(Screen).delete()
        session.query(Movie).delete()
        session.commit()
        
        print("Creating basic sample data...")
        
        # create 2 movies
        movies = [
            Movie(
                title="Oppenheimer", 
                genre="Biography", 
                duration=180
            ),
            Movie(
                title="It", 
                genre="Horror", 
                duration=135
            )
        ]
        session.add_all(movies)
        session.flush()
        print("Created 2 movies")
        
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
            for seat_num in range(1, 6):  # 5 seats per row
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
        
        # create 2 showtimes 
        from datetime import datetime, timedelta
        showtimes = []
        today = datetime.now().strftime("%Y-%m-%d")
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
            movie_id=movies[0].id,  # Oppenheimer
            screen_id=screens[0].id,
            show_time="16:00",
            show_date=tomorrow,  
            base_price=12.00,
            available_seats=50
        ))
        
        session.add_all(showtimes)
        session.flush()
        print("Created showtimes for today and tomorrow")
        
        # 3 basic snacks
        snacks = [
            Snack(name="Large Popcorn", category="popcorn", price=8.50, stock_quantity=50),
            Snack(name="Medium Soda", category="drinks", price=4.00, stock_quantity=100),
            Snack(name="Chocolate Candy", category="candy", price=4.50, stock_quantity=75)
        ]
        session.add_all(snacks)
        print("Created 3 snacks")
        
        
        session.commit()
        
        print("\nBasic sample data created successfully")
        print(f"Showtimes created for: {today} and {tomorrow}")
        
    except Exception as e:
        session.rollback()
        print(f"Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    create_basic_sample_data()