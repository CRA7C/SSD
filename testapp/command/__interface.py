from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """
    CommandInterface 클래스는 모든 명령어 클래스가 구현해야 하는 인터페이스를 정의합니다.
    """
    required_args_cnt: int = 0

    @abstractmethod
    def run(self, *args, **kwarg):
        """
        명령어를 실행하는 메서드입니다.
        """
        pass

    @staticmethod
    @abstractmethod
    def is_valid_args(*args, **kwarg):
        """
        명령어의 인자가 유효한지 확인하는 메서드입니다.

        Returns:
            bool: 인자가 유효한 경우 True, 그렇지 않으면 False
        """
        pass
