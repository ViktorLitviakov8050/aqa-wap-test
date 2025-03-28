import logging
import os
import datetime


class Logger:
    """Custom logging configuration for test automation framework"""
    
    _instance = None
    _logger = None
    
    @staticmethod
    def get_instance():
        """Singleton pattern to ensure only one logger instance"""
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance
    
    def __init__(self):
        """Initialize logger with custom formatting"""
        # Create logger
        self._logger = logging.getLogger("twitch_test_automation")
        self._logger.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create file handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
    
    def info(self, message):
        """Log info level message"""
        self._logger.info(message)
    
    def debug(self, message):
        """Log debug level message"""
        self._logger.debug(message)
    
    def warning(self, message):
        """Log warning level message"""
        self._logger.warning(message)
    
    def error(self, message):
        """Log error level message"""
        self._logger.error(message)
    
    def critical(self, message):
        """Log critical level message"""
        self._logger.critical(message)


# Convenience function to get logger instance
def get_logger():
    """Get the logger instance"""
    return Logger.get_instance() 