import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
import inspect
import re

LOG_FILE_PATH = Path(__file__).parent.parent / 'log' / 'latest.log'
LOG_MAX_SIZE = 10 * 1024


def print_function_name(func):
    """
    함수 실행 시 함수 이름을 출력하는 데코레이터 함수입니다.

    Args:
        func (function): 데코레이트할 함수

    Returns:
        function: 데코레이트된 함수
    """

    def wrapper(*args, **kwargs):
        Logger().debug(f"Executing function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class MyRotatingFileHandler(RotatingFileHandler):
    """
    로그 파일이 회전될 때 파일 이름을 변경하는 기능을 추가한 RotatingFileHandler 클래스입니다.
    """

    def doRollover(self):
        """
        로그 파일 회전을 수행하고 백업 파일 이름을 변경합니다.
        """
        super().doRollover()

        if self.is_already_bkup_file() is True:
            self.rename_log_to_zip(self.get_exact_log_name())

        self.rename_backup_files()

    def rename_backup_files(self):
        """
        백업 파일의 이름을 현재 날짜와 시간으로 변경합니다.
        """
        bkup_file_name = self.get_bkup_file_name()

        # RotatingFileHandler는 기본적으로 {로그파일이름}.1 .2 .3 이런식으로 백업파일 생성함
        for i in range(1, self.backupCount + 1):
            old_filename = f"{self.baseFilename}.{i}"
            if os.path.exists(old_filename):
                new_filename = os.path.join(os.path.dirname(self.baseFilename), bkup_file_name)
                if os.path.isfile(new_filename):
                    os.remove(new_filename)
                os.rename(old_filename, new_filename)

    def get_bkup_file_name(self):
        """
        백업 파일 이름을 생성합니다.

        Returns:
            str: 백업 파일 이름
        """
        return f'until_{datetime.now().strftime("%y%m%d_%H%M%S")}.log'

    def is_already_bkup_file(self) -> bool:
        """
        백업 파일이 이미 존재하는지 확인합니다.

        Returns:
            bool: 백업 파일이 이미 존재하면 True, 그렇지 않으면 False
        """
        find_pattern = r'until_(\d{6})_(\d{6})\.log'
        for filename in os.listdir(os.path.dirname(self.baseFilename)):
            if re.match(find_pattern, filename):
                return True
        return False

    def get_exact_log_name(self) -> str:
        """
        until_날짜_시간.log에 맵핑되는 정확한 로그파일 명을 반환합니다.

        Returns:
            str: until_날짜_시간.log 형식의 파일명 (경로포함 X)
        """
        find_pattern = r'until_(\d{6})_(\d{6})\.log'
        for filename in os.listdir(os.path.dirname(self.baseFilename)):
            if re.match(find_pattern, filename):
                return filename

    def rename_log_to_zip(self, filename):
        until_log_file_path = os.path.join(os.path.dirname(self.baseFilename), filename)
        zip_file_path = os.path.join(os.path.dirname(self.baseFilename), os.path.splitext(filename)[0] + ".zip")

        if os.path.isfile(zip_file_path):
            os.remove(zip_file_path)
        os.rename(until_log_file_path, zip_file_path)


class CustomFormatter(logging.Formatter):
    """
    로그 메시지 형식을 커스터마이징하는 Formatter 클래스입니다.
    """

    def format(self, record):
        """
        로그 레코드를 지정된 형식으로 포맷합니다.

        Args:
            record (logging.LogRecord): 로그 레코드

        Returns:
            str: 포맷된 로그 메시지
        """
        time_format = self.formatTime(record, "%y.%m.%d %H:%M")
        class_name = record.class_name
        func_name = record.func_name
        padded_function_name = f"{func_name}()"
        fixed_length = 30
        padded_function_name = padded_function_name.ljust(fixed_length)
        message = record.getMessage()

        return f"[{time_format}] {class_name}.{padded_function_name} : {message}"


class Logger:
    """
    싱글톤 패턴을 적용한 Logger 클래스입니다.
    """
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
            file_formatter = CustomFormatter()
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(console_handler)

    def info(self, message):
        """
        정보 로그 메시지를 기록합니다.

        Args:
            message (str): 기록할 메시지
        """
        self.log_with_class_func_name(logging.INFO, message)

    def debug(self, message):
        """
        디버그 로그 메시지를 기록합니다.

        Args:
            message (str): 기록할 메시지
        """
        self.log_with_class_func_name(logging.DEBUG, message)

    def warning(self, message):
        """
        경고 로그 메시지를 기록합니다.

        Args:
            message (str): 기록할 메시지
        """
        self.log_with_class_func_name(logging.WARNING, message)

    def error(self, message):
        """
        오류 로그 메시지를 기록합니다.

        Args:
            message (str): 기록할 메시지
        """
        self.log_with_class_func_name(logging.ERROR, message)

    def log_with_class_func_name(self, level, message):
        """
        클래스와 함수 이름을 포함하여 로그 메시지를 기록합니다.

        Args:
            level (int): 로그 레벨
            message (str): 기록할 메시지
        """
        frame = inspect.currentframe().f_back.f_back

        func_name = frame.f_code.co_name
        class_name = frame.f_locals['self'].__class__.__name__
        self.logger.log(level, message, extra={'class_name': class_name, 'func_name': func_name})
