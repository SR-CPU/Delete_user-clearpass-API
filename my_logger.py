"""

SR - CPU Design

"""

import logging
import logzero
from logzero import setup_logger

main_logger = setup_logger(name="main_logger", logfile="/var/log/guest_handler.log", level=logging.INFO)
