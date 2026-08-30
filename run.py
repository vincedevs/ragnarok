"""
Script for running the application

Run via the following command:

uv run python run.py
"""

from __future__ import annotations

import signal
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

BACKEND_DATA = BACKEND / "data"
UPLOADS = BACKEND_DATA / "uploads"
CHROMA = BACKEND_DATA / "chroma"
SHUTDOWN_TIMEOUT_SECONDS = 5


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


def stop_process(process: subprocess.Popen) -> None:
    """Stop a child process, escalating only if graceful shutdown times out."""
    if process.poll() is not None:
        return

    process.send_signal(signal.SIGINT)

    try:
        process.wait(timeout=SHUTDOWN_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.terminate()

        try:
            process.wait(timeout=SHUTDOWN_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def wait_for_exit(processes: tuple[subprocess.Popen, ...]) -> int:
    """Wait until a child exits and return its status code."""
    while True:
        for process in processes:
            return_code = process.poll()

            if return_code is not None:
                return return_code

        time.sleep(0.25)


def main() -> None:
    ensure_directories()
    ensure_env_files()

    backend = start_backend()
    frontend = start_frontend()

    processes = (backend, frontend)

    try:
        return_code = wait_for_exit(processes)

        if return_code != 0:
            raise SystemExit(return_code)
    except KeyboardInterrupt:
        print("\nStopping RAGnarok...")
    finally:
        for process in processes:
            stop_process(process)


if __name__ == "__main__":
    main()
