"""
통합 테스트를 위한 스크립트 입니다.(test double 사용하지 않음)
"""
import sys
from unittest import TestCase

from ssd.__main__ import SSDRunner
from ssd.nand_driver import NandDriver, NAND_FILE_PATH
from ssd.result_manager import RESULT_FILE_PATH


class TestSSDRunner(TestCase):
    def setUp(self):
        self.runner = SSDRunner()
        NandDriver.initiate_nand_file(NAND_FILE_PATH)

    def test_run_ssd_write_and_read(self):
        params = [
            (['test', 'W', '20', '0x1289CDEF'], ['test', 'R', '20'], '0x1289CDEF'),
            (['test', 'W', '10', '0xFF1100AA'], ['test', 'R', '10'], '0xFF1100AA'),
        ]
        for write_cmd, read_cmd, expected in params:
            with self.subTest(f"write cmd: {write_cmd}, read cmd: {read_cmd}"):
                sys.argv = write_cmd
                self.runner.run()

                sys.argv = read_cmd
                self.runner.run()
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
        ]
        for test_case, cmd in params:
            with self.subTest(test_case):
                sys.argv = cmd
                with self.assertRaises(ValueError):
                    self.runner.is_valid_command()
