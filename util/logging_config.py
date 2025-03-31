import structlog
import logging
from pathlib import Path


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Define processors
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        structlog.processors.JSONRenderer()  # JSON Renderer as the last processor
    ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Create handlers with a simple formatter
    formatter = logging.Formatter("%(message)s")  # Simple formatter
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Add handlers to the root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Reduce logging level for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

# import logging
# from pathlib import Path
#
#
# def setup_logging():
#     # Create a directory for logs
#     log_dir = Path("logs")
#     log_dir.mkdir(exist_ok=True)
#
#     # Log format configuration
#     log_formatter = logging.Formatter(
#         "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )
#
#     # Create a handler to write to file
#     file_handler = logging.FileHandler(log_dir / "app.log")
#     file_handler.setFormatter(log_formatter)
#     file_handler.setLevel(logging.INFO)
#
#     # Create a handler for output to console
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(log_formatter)
#     console_handler.setLevel(logging.DEBUG)
#
#     # Configuration of the root log
#     root_logger = logging.getLogger()
#     root_logger.setLevel(logging.DEBUG)
#     root_logger.addHandler(file_handler)
#     root_logger.addHandler(console_handler)
#
#     # Reduce logging level for third-party libraries
#     logging.getLogger("uvicorn").setLevel(logging.WARNING)
#     logging.getLogger("httpx").setLevel(logging.WARNING)
