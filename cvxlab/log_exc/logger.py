"""Logging utilities for CVXlab.

Provides the Logger class for consistent, colorized logging across the package.
Supports configurable formats, log levels, child loggers, and timing context managers.
"""
import logging
import time
import subprocess
import tempfile
import os

from contextlib import contextmanager
from datetime import datetime
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

    @contextmanager
    def convergence_monitor(
            self,
            output_dir: str,
            scenario_name: str = "N/A",
            tolerance: float = 0.001,
    ):
        """Context manager for convergence monitoring in a separate terminal.

        Creates a temporary file and opens a new terminal window to monitor
        convergence data in real-time.

        Args:
            output_dir (str): Directory for temporary convergence file.
            scenario_name (str): Name/coordinates of the scenario being solved.
            tolerance (float): Numerical tolerance threshold (as decimal).

        Yields:
            dict: Dictionary with 'log' method for writing convergence data.
        """
        # Create log file
        log_filename = f"convergence_{scenario_name}.log"
        convergence_file_path = os.path.join(output_dir, log_filename)

        if os.path.exists(convergence_file_path):
            os.remove(convergence_file_path)

        messages = []

        header_lines = [
            "="*79,
            f"CONVERGENCE MONITORING - Scenario: {scenario_name}",
            f"Tolerance: {tolerance*100:.3f}%",
            "="*79,
            ""
        ]

        with open(convergence_file_path, 'w') as f:
            for line in header_lines:
                f.write(line + "\n")
            f.flush()

        # Build PowerShell command
        ps_command = (
            f'while ($true) {{ '
            f'Clear-Host; '
            f'Get-Content "{convergence_file_path}"; '
            f'Start-Sleep -Seconds 1 '
            f'}}'
        )

        # Open terminal
        terminal_process = None
        try:
            terminal_process = subprocess.Popen(
                ['powershell', '-NoExit', '-Command', ps_command],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            self.logger.warning(
                f"Could not open convergence monitoring terminal: {e}")

        # Logger function
        def convergence_log(message: str):
            """Write message to convergence monitoring file and store it."""
            messages.append(message)

            with open(convergence_file_path, 'a') as f:
                f.write(message + "\n")
                f.flush()

        try:
            yield {'log': convergence_log, 'file': convergence_file_path, 'messages': messages}
        finally:
            # Write completion message
            footer_lines = [
                "",
                "="*79,
                "MONITORING COMPLETE",
            ]

            with open(convergence_file_path, 'a') as f:
                for line in footer_lines:
                    f.write(line + "\n")
                f.flush()


if __name__ == '__main__':

    import tempfile

    logger = Logger(log_level='INFO', log_format='minimal')
    logger.info("Starting convergence monitor test...")

    # Use temporary directory
    test_dir = tempfile.gettempdir()

    with logger.convergence_monitor(
        output_dir=test_dir,
        scenario_name="test_scenario",
        tolerance=0.001,
    ) as conv_monitor:

        conv_log = conv_monitor['log']

        # Simulate convergence iterations
        tables = ['table_1', 'table_2', 'table_3']

        # Write header
        header = "Iteration  " + "  ".join(f"{t:>8}" for t in tables)
        conv_log(header)
        conv_log("-" * len(header))

        # Simulate iterations with decreasing errors
        for iteration in range(1, 6):
            time.sleep(0.5)  # Simulate computation

            # Generate decreasing errors
            errors = [0.5 / (iteration + i) for i, _ in enumerate(tables)]
            values_str = "  ".join(
                f"{e*100:>7.3f}{'*' if e > 0.001 else ' '}"
                for e in errors
            )

            conv_log(f"Iter_{iteration:>2}    {values_str}")

            # Check convergence
            if all(e < 0.001 for e in errors):
                conv_log(f"Convergence reached")
                break

    logger.info("Test completed. Check the monitoring terminal.")

    for msg in conv_monitor['messages']:
        logger.info(msg)
