import os
import ast
import importlib
import sys
from typing import List, Tuple


class CommandInterfaceVisitor(ast.NodeVisitor):
    def __init__(self, interface_name: str):
        self.interface_name = interface_name
        self.found_classes = []

    def visit_ClassDef(self, node):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self.interface_name:
                self.found_classes.append(node.name)
        self.generic_visit(node)


def find_command_interface_classes(directory: str, interface_name: str) -> List[Tuple[str, List[str]]]:
    result = []
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != 'main.py':
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                node = ast.parse(file.read(), filename=filename)
                visitor = CommandInterfaceVisitor(interface_name)
                visitor.visit(node)
                if visitor.found_classes:
                    module_name = filename[:-3]  # .py 확장자 제거
                    result.append((module_name, visitor.found_classes))
    return result


def get_classes(class_info: List[Tuple[str, List[str]]]) -> List[object]:
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


if __name__ == '__main__':
    # 현재 디렉토리에서 CommandInterface를 상속받은 클래스를 찾는다.
    result = find_command_interface_classes('.', 'CommandInterface')

    for file, class_names in result:
        print(f"File: {file}, Class names: {class_names}")

    # 찾아낸 클래스를 객체로 생성
    for cls in get_classes(result):
        print(f"class: {cls}, Type: {type(cls)}")
        print(cls().run())
