import builtins
from unittest import TestCase
from unittest.mock import patch, mock_open
from ssd.nand_driver import NandDriver


class TestNandDriver(TestCase):
    def setUp(self):
        self.driver = NandDriver()

    @patch("builtins.open", new_callable=mock_open,
           read_data='0x00000000\n0x00000000\n0x00000000\n0x1298CDEF\n0x00000000')
    def test_read(self, _):
        ret = self.driver.read(3)
        self.assertEqual(0x1298CDEF, ret)
        builtins.open.assert_called_once()

    @patch("builtins.open")
    def test_write(self, _):
        self.driver.write(3, 0x1298CDEF)

        self.assertEqual(builtins.open.call_count, 2)
        builtins.open.assert_called_with(self.driver.nand_file_path, 'w', encoding='utf-8')

    def test_write_value(self):
        # 전체 데이터에서 지정 된 LBA 의 값만 변경하는지 확인하는 테스트
        fake_data = '0x00000000\n0x00000000\n0x00000000'
        expected_data = ['0x00000000\n', '0x1298CDEF\n', '0x00000000']
        with patch('builtins.open',
                   mock_open(read_data=fake_data)) as mocked_open:
            self.driver.write(1, 0x1298CDEF)
            mocked_open.assert_called_with(self.driver.nand_file_path, 'w', encoding='utf-8')

            handle = mocked_open()
            handle.writelines.assert_called_once_with(expected_data)

    @patch("builtins.open")
    def test_erase(self, _):
        self.driver.erase(3, 3)

        self.assertEqual(builtins.open.call_count, 2)
        builtins.open.assert_called_with(self.driver.nand_file_path, 'w', encoding='utf-8')

    def test_erase_value(self):
        # 전체 데이터에서 지정 된 LBA들의 값들이 0인지 테스트
        fake_data = '0x1345CDEF\n0x1345CDEF\n0x21345678\n'
        expected_data = ['0x1345CDEF\n', '0x00000000\n', '0x00000000\n']
        with patch('builtins.open',
                   mock_open(read_data=fake_data)) as mocked_open:
            self.driver.erase(1, 2)

            handle = mocked_open()
            handle.writelines.assert_called_once_with(expected_data)
