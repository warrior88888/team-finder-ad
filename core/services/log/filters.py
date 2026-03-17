import logging


class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARNING


class WarningAndAboveFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.WARNING
