import logging
import colorlog

def create_color_logger(name="logger"):
    """
    Create and return a colorized logger instance.

    Args:
        name (str): Name of the logger. Defaults to __name__.

    Returns:
        logging.Logger: Configured color logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger
