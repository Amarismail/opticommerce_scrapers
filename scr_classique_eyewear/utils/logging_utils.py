import logging
import time
import sys

class UtcIsoFormatter(logging.Formatter):
  """Custom logging.Formatter class for logging UTC time in ISO8601 format
  """
  
  # Use gmtime or universal coordinated time or utc
  converter = time.gmtime # must not include '()'
  
  # Format the time for this log event
  def formatTime(self, record, datefmt=None):
    ct = self.converter(record.created)
    if datefmt:
      s = time.strftime(datefmt, ct)
    else:
      # Default UTC ISO8601 format of "YYYY-mm-ddTHH:MM:SS.fffZ"
      t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
      s = f"{t}.{record.msecs:03.0f}Z"
    return s

def setup_in_program_logging(out_logging_file_path='app.log', console_log_output="stderr"):
    """
    Set up logging configuration globally for the logging module.
    """
    from logging.handlers import RotatingFileHandler
    # Set global logging configuration
    logging.getLogger().setLevel(logging.DEBUG)
    
    format = '[%(asctime)s] {%(module)s:%(lineno)4s} %(levelname)-6s - %(message)s'
    formatter = UtcIsoFormatter(format)
    
    # Use UTC time for logs
    formatter.converter = time.gmtime

    # Create console handler
    if console_log_output == "stdout":
        console_log_output = sys.stdout
    elif console_log_output == "stderr":
        console_log_output = sys.stderr
    else:
        logging.error(f"Failed to set console output: invalid output '{console_log_output}'")
        return False

    console_handler = logging.StreamHandler(console_log_output)
    console_handler.setLevel(logging.INFO)  # Set console handler to a lower level if desired
    console_handler.setFormatter(formatter)

    # Create rotating file handler
    file_handler = RotatingFileHandler(
        filename=out_logging_file_path, 
        mode='w', 
        maxBytes=10485760,  # 10MB
        backupCount=20
    )
    file_handler.setLevel(logging.DEBUG)  # Log to file at INFO level
    file_handler.setFormatter(formatter)

    # Add handlers to the root logger
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)

def setup_logging(
    default_logging_file_path='logging.yaml',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    import os, sys
    import logging.config

    path = default_logging_file_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        import yaml
        
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        setup_in_program_logging()