from unittest import TestCase

from ssd.command import CommandFactory
from ssd.command_buffer import CommandBuffer


class TestCommandBuffer(TestCase):
    def setUp(self):
        super().setUp()
        self.cmd_buffer = CommandBuffer()

    def test_optimize(self):
        test_commands = [
            ('W', '1', '10'),  # 주소 1에 값 0x0A을 씀
            ('W', '5', '20'),  # 주소 5에 값 0x14을 씀
            ('E', '3', '4'),  # 주소 3부터 4칸 지움 (3, 4, 5, 6)
            ('W', '3', '30'),  # 주소 3에 값 0x1E을 씀
            ('E', '8', '2'),  # 주소 8부터 2칸 지움 (8, 9)
            ('E', '1', '2'),  # 주소 1부터 2칸 지움 (1, 2)
            ('W', '9', '40'),  # 주소 9에 값 0x28을 씀
            ('W', '12', '50'),  # 주소 12에 값 0x32을 씀
            ('E', '11', '3'),  # 주소 11부터 3칸 지움 (11, 12, 13)
            ('E', '10', '2'),  # 주소 10부터 2칸 지움 (10, 11)
            ('W', '10', '60')  # 주소 10에 값 0x3C을 씀
        ]
        test_data = [CommandFactory().parse_command(t) for t in test_commands]

        for t in test_data:
            self.cmd_buffer.push_command(t)

        expected_result = """E 3 4
W 3 30
E 8 2
E 1 2
W 9 40
E 11 3
E 10 2
W 10 60
"""

        actual_result = self.cmd_buffer.get_saved_data()
        self.assertEqual(expected_result, actual_result)


