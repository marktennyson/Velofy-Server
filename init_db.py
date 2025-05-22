# init_db.py
from database import create_db_and_tables

if __name__ == "__main__":
    create_db_and_tables()
    print("Tables created successfully.")
    print("You can now run the server using 'python server.py'")
    print("Make sure to set the MEDIA_DIR environment variable to the directory where your media files are stored.")