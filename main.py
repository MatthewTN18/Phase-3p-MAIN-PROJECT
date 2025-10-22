"""
Main entry point for the self-service cinema kiosk
"""

from src.cli.app import CinemaKiosk

def main():
    app = CinemaKiosk()
    app.run()

if __name__ == "__main__":
    main()