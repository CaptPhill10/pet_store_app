import logging
import sys
import structlog

# Standard Python logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/pet_store.log", encoding="utf-8"),
    ],
)

# Reduce logging level for third-party libraries
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# structlog setting
structlog.configure(
    processors=[
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer(colors=False),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Create global logger
logger = structlog.get_logger()
