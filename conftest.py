import httpx
import os
from uvicorn import run
import threading
import pytest
import random
import time
import structlog
from api.app import app
from util.logging_config import setup_logging

# Logging
setup_logging()
logger = structlog.get_logger(__name__)  # Use structlog


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """
    Start mock server using uvicorn.run and wait for it to be ready.
    """
    server_port = random.randint(10000, 60000)
    os.environ["PET_STORE_PORT"] = str(server_port)

    def run_server():
        logger.info("Starting server", server_port=server_port)
        try:
            run(app, host="127.0.0.1", port=server_port, log_level="info", loop="asyncio")
        except Exception as e:
            logger.error("Failed to start server", error=str(e))
            raise

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    logger.info("Server thread started", port=server_port)

    # Wait for server to be ready
    server_url = f"http://127.0.0.1:{server_port}/docs"
    for _ in range(10):
        try:
            response = httpx.get(server_url, timeout=1.0)
            if response.status_code == 200:
                logger.info("Server is up and running", url=server_url)
                break
        except httpx.RequestError:
            logger.warning("Attempt to connect to server failed", attempt=_ + 1)
            time.sleep(0.5)
    else:
        logger.error("Server didn't start", url=server_url)
        raise RuntimeError("Mock server failed to start")

    yield

    logger.info("Server fixture cleanup")


@pytest.fixture(scope="session")
def base_url():
    """Get dynamic base_url with server port."""
    port = os.environ.get("PET_STORE_PORT")
    if not port:
        logger.error("PET_STORE_PORT environment variable not installed")
        raise RuntimeError("PET_STORE_PORT environment variable not installed")
    base_url = f"http://127.0.0.1:{port}"
    logger.info("Base URL", base_url=base_url)
    return base_url
