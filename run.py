"""
Script for running the application

Run via the following command:

uv run python run.py
"""

from __future__ import annotations

import signal
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

BACKEND_DATA = BACKEND / "data"
UPLOADS = BACKEND_DATA / "uploads"
CHROMA = BACKEND_DATA / "chroma"


def ensure_directories() -> None:
    """Create required directories if they don't exist yet"""
    for directory in (BACKEND_DATA, UPLOADS, CHROMA):
        directory.mkdir(parents=True, exist_ok=True)


def ensure_env_files() -> None:
    """Verify require .env files exist"""
    backend_env = BACKEND / ".env"
    frontend_env = FRONTEND / ".env"

    if not backend_env.exists():
        raise FileNotFoundError("backend/.env not found!")

    if not frontend_env.exists():
        raise FileNotFoundError("frontend/.env not found!")


def start_backend() -> subprocess.Popen:
    return subprocess.Popen(
        ["uv", "run", "uvicorn", "app.main:app", "--reload"], cwd=BACKEND
    )


def start_frontend() -> subprocess.Popen:
    return subprocess.Popen(["uv", "run", "streamlit", "run", "Home.py"], cwd=FRONTEND)


def main() -> None:
    ensure_directories()
    ensure_env_files()

    backend = start_backend()
    frontend = start_frontend()

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nStopping RAGnarok...")

        backend.send_signal(signal.SIGINT)
        frontend.send_signal(signal.SIGINT)


if __name__ == "__main__":
    main()
