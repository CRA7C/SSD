import os
import ast
import sys
import logging
import importlib
import subprocess
from typing import List, Tuple

SCRIPTS_DIRECTORY = os.path.dirname(__file__)


class CommandInterfaceVisitor(ast.NodeVisitor):
    def __init__(self, interface_name: str):
        self.interface_name = interface_name
        self.found_classes = []

    def visit_ClassDef(self, node):  # do not change the overwrite method name.
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self.interface_name:
                self.found_classes.append(node.name)
        self.generic_visit(node)


def find_command_classes(interface_name: str) -> List[Tuple[str, List[str]]]:
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
    class_info = find_command_classes('CommandInterface')
    ret_dict = {}
    for module_name, class_names in class_info:
        for class_name in class_names:
            ret_dict[class_name] = os.path.abspath(f"{module_name}.py")
    return ret_dict


def get_classes() -> List[object]:
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
    try:
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        # result.returncode가 0이면 성공, 그렇지 않으면 실패
        logging.debug(result.stdout)
        if result.stderr:
            logging.error(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running script: {e}")
        return False


if __name__ == '__main__':
    from pprint import pprint
    script_dict = get_test_scripts()
    pprint(script_dict)
    res = run_script(script_dict['TestApp1'])
    print(res)
