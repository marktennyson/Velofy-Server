"""
This is a simple FastAPI application that serves as the backend for a web application.

Features:
- User authentication using JWT.
- Media management endpoints.
- Health check endpoint.
- Database interactions using SQLModel.
- Data validation with Pydantic.
- Custom exception handling for missing version file errors.

Design:
- Structured for easy expansion and modification.
- Intended to run with Uvicorn (a lightning-fast ASGI server).
- Optimized for development environments with hot reloading enabled.
"""
# server.py
# This script runs the FastAPI application using Uvicorn.

import uvicorn as uv

if __name__ == "__main__":
    uv.run("app.app:app", host="0.0.0.0", port=8000, reload=True)