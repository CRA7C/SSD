import os
import ast
import sys
import importlib
import subprocess
from typing import List, Tuple
from testapp.constants import SCRIPTS_DIRECTORY
from my_logger import Logger

logger = Logger()


class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found_classes = []

    def visit_ClassDef(self, node):
        self.found_classes.append(node.name)
        self.generic_visit(node)


def find_classes() -> List[Tuple[str, List[str]]]:
    """
    주어진 디렉토리 내의 모든 파이썬 파일에서 정의된 클래스를 찾습니다.
    Returns:
        List[Tuple[str, List[str]]]: 모듈 이름과 클래스 이름 리스트의 튜플 리스트
    """
    directory = SCRIPTS_DIRECTORY
    result = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith("_"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                node = ast.parse(file.read(), filename=filename)
                visitor = ClassVisitor()
                visitor.visit(node)
                if visitor.found_classes:
                    module_name = filename[:-3]  # .py 확장자 제거
                    result.append((module_name, visitor.found_classes))
    return result


def get_test_scripts() -> dict[str, str]:
    """
    테스트 스크립트를 반환합니다.

    Returns:
        Dict[str, str]: 테스트 스크립트 딕셔너리 {테스트 이름: 스크립트 절대 경로}
    """
    class_info = find_classes()
    ret_dict = {}
    for module_name, class_names in class_info:
        for class_name in class_names:
            ret_dict[class_name] = SCRIPTS_DIRECTORY / f"{module_name}.py"
    return ret_dict


def get_classes() -> List[object]:
    """
    CommandInterface를 구현한 클래스 객체들을 반환합니다.

    Returns:
        List[object]: 클래스 객체 리스트
    """
    class_info = find_classes()
    class_list = []
    original_sys_path = sys.path.copy()
    try:
        sys.path.append(os.getcwd())  # 현재 디렉토리를 sys.path에 추가
        for module_name, class_names in class_info:
            module = importlib.import_module(module_name)
            for class_name in class_names:
                class_list.append(getattr(module, class_name))
    finally:
        sys.path = original_sys_path  # 원래 sys.path 복원
    return class_list


def run_script(script_name: str, use_print: bool = False) -> bool:
    """
    주어진 스크립트를 실행합니다.

    Args:
        script_name (str): 실행할 스크립트 이름
        use_print (bool): 콘솔 창에 출력할지 말지 결정

    Returns:
        bool: 스크립트 실행 성공 여부
    """
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        # result.returncode가 0이면 성공, 그렇지 않으면 실패
        if result.stdout:
            if use_print:
                print(result.stdout)
            else:
                logger.debug(result.stdout)
        if result.stderr:
            logger.debug(result.stderr)
        return result.returncode == 0
    except Exception as e:
        logger.debug(f"Error running script: {e}")
        return False


def run_test_script_file(list_file: str):
    """
    주어진 파일에 있는 테스트 스크립트를 순차적으로 실행합니다.

    Args:
        list_file (str): 테스트 스크립트 목록 파일
    """
    ts_dict = get_test_scripts()
    with open(list_file, 'r', encoding='utf-8') as f:
        for test_id in f.readlines():
            test_id = test_id.strip()
            print(f"{test_id:30} --- ", end="")
            if test_id in ts_dict.keys():
                print("Run...", end="", flush=True)
                if run_script(ts_dict[test_id]):
                    print('PASS')
                else:
                    print('FAIL!')
            else:
                print("NOT FOUND!")


if __name__ == '__main__':
    from pprint import pprint

    script_dict = get_test_scripts()
    pprint(script_dict)
    res = run_script(script_dict['TestApp1'])
    print(res)
