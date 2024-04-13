import sys
from loguru import logger


logger.remove() #清空預設值

fmt = "<b><g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level:<8}</lvl> | <e>{file}:{line:<4}</e> | <lvl>{message}</lvl></b>"
logger.add(sys.stdout, format=fmt)