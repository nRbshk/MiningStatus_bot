import logging
logger = logging.getLogger(__name__)
def get_token(fn: str = "token.token") -> str:
    logger.info("Getting token")
    return open(fn,'r').readline()

