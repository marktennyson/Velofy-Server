🎬 Velofy The Home Media Server
================

**Velofy** is a robust, extensible backend server for **media management and streaming**, built with [FastAPI](https://fastapi.tiangolo.com/). It provides 🔒 secure user authentication, 🎥 efficient media handling, and a modern API for web and mobile clients. Designed for rapid development and seamless integration with your home media setup, Velofy is your personal Netflix-style media server. 🚀

* * *

✨ Features
----------

*   🔐 **User Authentication** – JWT-based login, registration & profile management.
*   🎞️ **Media Management** – List, search, stream, and manage movies.
*   📼 **Watch History** – Track and update watch progress per user.
*   🧠 **Metadata Extraction** – Auto-fetch movie metadata from IMDb.
*   🗃️ **Database Integration** – ORM with SQLModel (SQLAlchemy + Pydantic).
*   🚨 **Custom Exception Handling** – Consistent and clear error responses.
*   ❤️ **Health & Version Endpoints** – Easy monitoring and CI/CD support.
*   ⚙️ **Dev Ready** – Hot reloading, easy debugging, modular structure.
*   🧱 **Extensible Architecture** – Plug-and-play new features or endpoints.
*   ✅ **CI/CD Friendly** – Includes linting workflows for code quality.

* * *

📁 Project Structure
--------------------

    Velofy-Server/
    ├── app/
    │   ├── app.py
    │   └── routes/
    │       ├── auth.py
    │       └── movies.py
    ├── jobs/
    │   └── movie/
    │       ├── interfaces.py
    │       └── metadata_extractor.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── auth.py
    │   └── movies.py
    ├── models.py
    ├── database.py
    ├── exceptions.py
    ├── app_config.py
    ├── init_db.py
    ├── server.py
    ├── movie_metadata.json
    ├── requirements.txt
    ├── VERSION
    ├── LICENSE
    └── .github/
        └── workflows/
            └── pylint.yml

* * *

🚀 Getting Started
------------------

### 1\. 🧾 Clone the Repository

    git clone https://github.com/yourusername/Velofy-Server.git
    cd Velofy-Server

### 2\. 📦 Install Dependencies

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### 3\. ⚙️ Configure Environment

Edit `app_config.py` or set environment variables:

*   `MEDIA_DIR`: Path to your media folder (default: `./media`)
*   `MOVIE_MEDIA_DIR`: Folder for movie files (default: `./media/movies`)
*   `SECRET_KEY`: JWT signing secret

### 4\. 🗄️ Initialize the Database

    python init_db.py

### 5\. 🧠 Extract Movie Metadata (Optional)

    python jobs/movie/metadata_extractor.py --media-path /path/to/your/movies

### 6\. ▶️ Run the Server

    python server.py

Visit: [http://localhost:8000](http://localhost:8000)

* * *

📡 API Overview
---------------

### 🔐 Authentication

*   `POST /auth/login` – Login & get JWT
*   `POST /auth/register` – Create new user
*   `GET /auth/me` – View profile (auth required)
*   `PUT /auth/me` – Update profile
*   `DELETE /auth/me` – Delete account

### 🎬 Movies & Media

*   `GET /media/movies/` – List movies (filter, sort, paginate)
*   `GET /media/movie/{id}` – Get movie details
*   `GET /media/stream/{id}` – Stream movie file
*   `GET /media/subtitle/{id}` – Download subtitles
*   `POST /media/watch/{id}` – Log watch entry
*   `PUT /media/watch/{id}` – Update watch progress
*   `GET /media/watch/{id}` – View watch status

### 💓 Health & Version

*   `GET /health` – Health check
*   `GET /version` – App version

* * *

🧬 Database Models
------------------

*   **User** – Login credentials and profile
*   **Movie** – Metadata and media path
*   **Cast** – Actor/director info
*   **WatchHistory** – Progress tracking
*   **MovieCastLink** – M:N relationship table

* * *

🧠 Metadata Extraction
----------------------

The script `metadata_extractor.py` scans your movie folder, uses IMDb APIs, and creates structured JSON. Type definitions are in `interfaces.py`.

* * *

🧑‍💻 Development
-----------------

*   🔁 **Hot Reload** – Enabled via Uvicorn
*   🧹 **Linting** – Uses Pylint (CI pipeline)
*   🧪 **Testing** – Add unit tests via `pytest` or `unittest`
*   ⚙️ **Config** – All in `app_config.py`

* * *

📦 Deployment
-------------

*   Use **Uvicorn** or **Gunicorn** with Nginx in production
*   Set `reload=False` and use a strong `SECRET_KEY`
*   Recommended: PostgreSQL for production database

* * *

🤝 Contributing
---------------

Contributions are welcome! 🛠️

*   Please lint your code
*   Use meaningful commit messages
*   Open an issue for major changes

* * *

📜 License
----------

Licensed under the **MIT License**. See `LICENSE` for details.

* * *

🙏 Acknowledgements
-------------------

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [SQLModel](https://sqlmodel.tiangolo.com/)
*   [Cinemagoer (IMDbPY)](https://cinemagoer.github.io/)
*   [Pydantic](https://docs.pydantic.dev/)
*   [Uvicorn](https://www.uvicorn.org/)

* * *

📬 Contact
----------

For help or feedback, open an issue or contact the maintainer via GitHub.

**🍿 Happy streaming with Velofy!**
