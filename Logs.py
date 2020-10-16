import logging
import sys

loggers = {}

def setup_logger(name, log_file, level=logging.DEBUG, console=True):
    """To setup as many loggers as you want"""
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        if console:
            logger.addHandler(logging.StreamHandler(sys.stdout))
        loggers[name] = logger

        return logger
