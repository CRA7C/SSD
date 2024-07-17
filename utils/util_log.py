import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
import inspect

LOG_FILE_PATH = Path(__file__).parent.parent / 'log' / f'latest.log'
LOG_MAX_SIZE = 10 * 1024

def print_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"Executing function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class MyRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        # 기본 회전 작업 수행
        super().doRollover()

        self.is_already_bkup_file()

        self.rename_backup_files()

    def rename_backup_files(self):
        base_filename = self.baseFilename
        base_file_dir = os.path.dirname(base_filename)
        bkup_file_name = self.get_bkup_file_name()

        # RotatingFileHandler는 기본적으로 {로그파일이름}.1 .2 .3 이런식으로 백업파일 생성함
        for i in range(1, self.backupCount + 1):
            old_filename = f"{base_filename}.{i}"
            if os.path.exists(old_filename):
                new_filename = os.path.join(base_file_dir, bkup_file_name)
                os.rename(old_filename, new_filename)

    def get_bkup_file_name(self):
        return f'until_{datetime.now().strftime("%y%m%d_%H%M%S")}.log'

    def is_already_bkup_file(self) -> bool:
        pass


class CustomFormatter(logging.Formatter):
    def format(self, record):
        time_format = self.formatTime(record, "%y.%m.%d %H:%M")
        class_name = record.class_name
        func_name = record.func_name
        padded_function_name = f"{func_name}()"
        fixed_length = 30
        padded_function_name = padded_function_name.ljust(fixed_length)
        message = record.getMessage()

        return f"[{time_format}] {class_name}.{padded_function_name} : {message}"


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger('myLogger')
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            log_dir = os.path.dirname(LOG_FILE_PATH)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = MyRotatingFileHandler(LOG_FILE_PATH, maxBytes=LOG_MAX_SIZE, backupCount=1)
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = CustomFormatter()
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.log_with_class_func_name(logging.INFO, message)

    def debug(self, message):
        self.log_with_class_func_name(logging.DEBUG, message)

    def warning(self, message):
        self.log_with_class_func_name(logging.WARNING, message)

    def error(self, message):
        self.log_with_class_func_name(logging.ERROR, message)

    def log_with_class_func_name(self, level, message):
        frame = inspect.currentframe().f_back.f_back

        func_name = frame.f_code.co_name
        class_name = frame.f_locals['self'].__class__.__name__
        self.logger.log(level, message, extra={'class_name': class_name, 'func_name': func_name})
