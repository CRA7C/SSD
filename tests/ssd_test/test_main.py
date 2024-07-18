"""
통합 테스트를 위한 스크립트 입니다.(test double 사용하지 않음)
"""
import sys
from unittest import TestCase

from ssd.__main__ import SSDRunner
from ssd.result_manager import RESULT_FILE_PATH
from ssd.command import CommandFactory


class TestSSDRunner(TestCase):
    def setUp(self):
        self.runner = SSDRunner()

    def test_run_ssd_write_and_read(self):
        params = [
            (['W', '20', '0x1289CDEF'], ['R', '20'], '0x1289CDEF'),
            (['W', '10', '0xFF1100AA'], ['R', '10'], '0xFF1100AA'),
        ]
        for write_cmd, read_cmd, expected in params:
            with self.subTest(f"write cmd: {write_cmd}, read cmd: {read_cmd}"):
                cmd = CommandFactory.parse_command(write_cmd)
                self.runner.run(cmd)

                cmd = CommandFactory.parse_command(read_cmd)
                self.runner.run(cmd)
                with open(RESULT_FILE_PATH, 'r') as f:
                    actual = f.read()

                self.assertEqual(expected, actual)

    def test_run_ssd_with_invalid_cmd(self):
        params = [
            ('시스템 인자 없음.', ['test']),
            ('LBA 인자 없음.', ['test', 'R']),
            ('R이나 W가 아닌 명령어.', ['test', 'r', '20']),
            ('숫자가 아닌 LBA.', ['test', 'R', 'aa']),
            ('범위를 벗어난 LBA.', ['test', 'R', '-1']),
            ('value가 없는 write.', ['test', 'W', '20']),
            ('8자리가 아닌 value', ['test', 'W', '20', '0x1289']),
            ('0x가 없는 value', ['test', 'W', '20', '111289CDEF']),
            ('16진수가 아닌 value', ['test', 'W', '20', '0xZ289CDEF']),
            ('value가 없는 erase.', ['test', 'E', '20']),
            ('10초과인 size', ['test', 'E', '20', '11']),
            ('1미만인 size', ['test', 'E', '20', '0']),
            ('숫자가 아닌 size', ['test', 'E', '20', 'a']),
        ]
        for test_case, cmd in params:
            with self.subTest(test_case):
                sys.argv = cmd
                with self.assertRaises(ValueError):
                    CommandFactory.parse_command(sys.argv)

    def test_run_ssd_write_erase_read(self):
        write_cmd = ['W', '0', '0x1289CDEF']
        read_cmd = ['R', '0']
        erase_cmd = ['E', '0', '10']
        expected_write = '0x1289CDEF'
        expected_erase = '0x00000000'

        sys.argv = write_cmd
        for i in range(0, 50):
            sys.argv[1] = str(i)
            cmd = CommandFactory.parse_command(sys.argv)
            self.runner.run(cmd)

        cmd = CommandFactory.parse_command(erase_cmd)
        self.runner.run(cmd)

        sys.argv = read_cmd
        for i in range(0, 10):
            sys.argv[1] = str(i)
            cmd = CommandFactory.parse_command(sys.argv)
            self.runner.run(cmd)

            with open(RESULT_FILE_PATH, 'r') as f:
                actual = f.read()
            self.assertEqual(expected_erase, actual)

        for i in range(11, 50):
            sys.argv[1] = str(i)
            cmd = CommandFactory.parse_command(sys.argv)
            self.runner.run(cmd)

            with open(RESULT_FILE_PATH, 'r') as f:
                actual = f.read()
            self.assertEqual(expected_write, actual)


    def test_run_ssd_write_erase_read_for_buffer_optimization(self):
        test_commands = [
            ('W', '1', '0x0000000A'),  # 주소 1에 값 0x0A을 씀
            ('W', '5', '0x00000014'),  # 주소 5에 값 0x14을 씀
            ('E', '3', '4'),  # 주소 3부터 4칸 지움 (3, 4, 5, 6)
            ('W', '3', '0x0000001E'),  # 주소 3에 값 0x1E을 씀
            ('E', '8', '2'),  # 주소 8부터 2칸 지움 (8, 9)
            ('E', '1', '2'),  # 주소 1부터 2칸 지움 (1, 2)
            ('W', '9', '0x00000028'),  # 주소 9에 값 0x28을 씀
            ('W', '12', '0x00000032'),  # 주소 12에 값 0x32을 씀
            ('E', '11', '3'),  # 주소 11부터 3칸 지움 (11, 12, 13)
            ('E', '10', '2'),  # 주소 10부터 2칸 지움 (10, 11)
            ('W', '10', '0x0000003C')  # 주소 10에 값 0x3C을 씀
        ]

        for t_cmd in test_commands:
            self.runner.run(CommandFactory.parse_command(t_cmd))

        self.runner.run(CommandFactory.parse_command(['F']))

