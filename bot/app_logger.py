from loguru import logger
import sys

logger.remove()
# logger.add("logs.log", level="DEBUG")
logger.add(sys.stdout, level="DEBUG")

