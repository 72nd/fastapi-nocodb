from .config import settings

import logging


logging.basicConfig(level=settings.log_level.upper())


logger = logging.getLogger()