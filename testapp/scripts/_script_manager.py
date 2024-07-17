import os
import ast
import sys
import logging
import importlib
import subprocess
from typing import List, Tuple
from testapp.constants import SCRIPTS_DIRECTORY


class CommandInterfaceVisitor(ast.NodeVisitor):
    """
    CommandInterfaceVisitor 클래스는 주어진 인터페이스를 구현한 클래스들을 찾기 위한 AST 노드 방문자입니다.

    .. note:
        ast: Abstract Syntax Trees. 파이썬 추상 구문 문법의 트리 처리 도구

    Attributes:
        interface_name (str): 찾고자 하는 인터페이스 이름
        found_classes (List[str]): 발견된 클래스 이름 리스트
    """
    def __init__(self, interface_name: str):
        self.interface_name = interface_name
        self.found_classes = []

    def visit_ClassDef(self, node):  # do not change the overwrite method name.
        """
        AST (Abstract Syntax Trees) 에서 클래스 정의 노드를 방문합니다.

        Args:
            node (ast.ClassDef): 클래스 정의 노드
        """
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self.interface_name:
                self.found_classes.append(node.name)
        self.generic_visit(node)


def find_command_classes(interface_name: str) -> List[Tuple[str, List[str]]]:
    """
    주어진 인터페이스를 구현한 클래스를 찾습니다.

    Args:
        interface_name (str): 인터페이스 이름

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
                visitor = CommandInterfaceVisitor(interface_name)
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
    class_info = find_command_classes('CommandInterface')
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
    class_info = find_command_classes('CommandInterface')
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


def run_script(script_name: str) -> bool:
    """
    주어진 스크립트를 실행합니다.

    Args:
        script_name (str): 실행할 스크립트 이름

    Returns:
        bool: 스크립트 실행 성공 여부
    """
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        # result.returncode가 0이면 성공, 그렇지 않으면 실패
        # TODO: 추후 Logger 변경 필요!
        logging.debug(result.stdout)
        if result.stderr:
            logging.error(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running script: {e}")
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
