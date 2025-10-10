"""Logging utilities for CVXlab.

Provides the Logger class for consistent, colorized logging across the package.
Supports configurable formats, log levels, child loggers, and timing context managers.
"""

import logging
import time

from contextlib import contextmanager
from typing import Literal


class Logger:
    """Logger class for CVXlab applications.

    Supports configurable log formats, colorized output, and hierarchical child 
    loggers. Provides convenience methods for logging at different levels and 
    timing code execution.

    Attributes:
    - log_format (str): Selected log format key.
    - str_format (str): Log format string.
    - logger (logging.Logger): Underlying Python logger instance.
    """

    LEVELS = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    FORMATS = {
        'minimal': '%(levelname)s | %(message)s',
        'standard': '%(levelname)s | %(name)s | %(message)s',
        'detailed': '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    }

    COLORS = {
        'WARNING': '\033[38;5;214m',    # Orange
        'ERROR': '\033[31m',            # Red
        'DEBUG': '\033[32m',            # Green
        'RESET': '\033[0m',             # Reset to default
    }

    def __init__(
            self,
            logger_name: str = 'default_logger',
            log_level: Literal['INFO', 'DEBUG', 'WARNING', 'ERROR'] = 'INFO',
            log_format: Literal[
                'minimal', 'standard', 'detailed'] = 'standard',
    ):
        """Initialize a Logger instance.

        Args:
            logger_name (str): Name for the logger (default: 'default_logger').
            log_level (str): Logging level ('INFO', 'DEBUG', etc.; default: 'INFO').
            log_format (str): Format style for log messages ('minimal', 'standard', 'detailed').
        """
        self.log_format = log_format
        self.str_format = self.FORMATS[log_format]
        self.logger = logging.getLogger(logger_name)

        if isinstance(log_level, str):
            level = self.LEVELS.get(log_level.upper(), logging.INFO)
        else:
            level = log_level

        self.logger.setLevel(level)

        if not self.logger.handlers:
            self.logger.setLevel(log_level)
            formatter = logging.Formatter(self.str_format)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(log_level)
            stream_handler.setFormatter(self.get_colors(formatter))
            self.logger.addHandler(stream_handler)

    def get_colors(self, formatter) -> logging.Formatter:
        """Wrap a formatter to apply ANSI colors based on log level.

        Args:
            formatter (logging.Formatter): Formatter to wrap.

        Returns:
            logging.Formatter: Formatter with colorized output.
        """
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                color = Logger.COLORS.get(record.levelname, '')
                reset = Logger.COLORS['RESET']
                formatted = super().format(record)
                return f"{color}{formatted}{reset}"

        return ColoredFormatter(formatter._fmt)

    def get_child(self, name: str) -> 'Logger':
        """Create a child Logger inheriting configuration from this logger.

        Args:
            name (str): Child logger name (typically module __name__).

        Returns:
            Logger: Configured child Logger instance.
        """
        child_logger = self.logger.getChild(name.split('.')[-1])

        new_logger = Logger(
            logger_name=child_logger.name,
            log_level=child_logger.level,
            log_format=self.log_format,
        )

        new_logger.logger.propagate = False
        return new_logger

    def log(self, message: str, level: str = logging.INFO) -> None:
        """Log a message at a specified level.

        Args:
            message (str): Message to log.
            level (str): Logging level (default: logging.INFO).
        """
        self.logger.log(msg=message, level=level)

    def info(self, message: str):
        """Log a message at INFO level.

        Args:
            message (str): Message to log.
        """
        self.logger.log(msg=message, level=logging.INFO)

    def debug(self, message: str):
        """Log a message at DEBUG level.

        Args:
            message (str): Message to log.
        """
        self.logger.log(msg=message, level=logging.DEBUG)

    def warning(self, message: str):
        """Log a message at WARNING level.

        Args:
            message (str): Message to log.
        """
        self.logger.log(msg=message, level=logging.WARNING)

    def error(self, message: str):
        """Log a message at ERROR level.

        Args:
            message (str): Message to log.
        """
        self.logger.log(msg=message, level=logging.ERROR)

    @contextmanager
    def log_timing(
            self,
            message: str,
            level: str = 'info',
            log_format: str = None,
            success: bool = True,
    ):
        """Context manager to log timing and status of a code block.

        Logs start, completion (with duration), and failure if an exception occurs.

        Args:
            message (str): Message describing the timed block.
            level (str): Log level for timing messages (e.g., 'info', 'debug').
            log_format (str, optional): Temporary log format for this block.
            success (bool, optional): Initial success status (default: True).

        Yields:
            dict: Status dictionary with 'success' key.
        """
        log_level = self.LEVELS.get(level.upper(), logging.INFO)
        log_function = getattr(
            self.logger,
            logging.getLevelName(log_level).lower()
        )

        log_function(message)
        status = {'success': success}

        if log_format:
            original_formatter = self.logger.handlers[0].formatter
            formatter = logging.Formatter(log_format)
            self.logger.handlers[0].setFormatter(formatter)
        else:
            original_formatter = None

        start_time = time.time()

        try:
            yield status
        except Exception:
            status['success'] = False
            raise
        finally:
            end_time = time.time()
            duration = end_time - start_time
            duration_str = \
                f"{int(duration // 60)}m {int(duration % 60)}s" \
                if duration > 60 else f"{duration:.2f} seconds"

            if status['success']:
                log_function(f"{message} DONE ({duration_str})")
            else:
                log_function(f"{message} FAILED ({duration_str})")

            if log_format:
                self.logger.handlers[0].setFormatter(original_formatter)


if __name__ == '__main__':
    logger = Logger(log_level='INFO', log_format='minimal')

    try:
        with logger.log_timing("Outer block"):
            with logger.log_timing("Inner block"):
                raise RuntimeError("Simulated failure")

    except RuntimeError as e:
        logger.error(f"Caught exception: {e}")
