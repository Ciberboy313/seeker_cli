import unittest
from unittest.mock import patch
import os
import shutil
from core.tools import (
    tool_list_dir,
    tool_launch_program
)

class TestNewTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_env"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("Hello World")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_list_dir(self):
        output = tool_list_dir(self.test_dir)
        self.assertIn("file1.txt", output)
        self.assertIn("subdir", output)

    @patch('core.tools._open_path')
    @patch('core.tools._find_executable')
    def test_launch_program_success(self, mock_find, mock_open):
        """Tests that launch_program calls find and then open on success."""
        fake_program = "test.exe"
        fake_path = "C:\\Tools\\test.exe"
        
        mock_find.return_value = fake_path
        mock_open.return_value = f"'{fake_program}' avviato con successo."

        result = tool_launch_program(fake_program)

        mock_find.assert_called_once_with(fake_program)
        mock_open.assert_called_once_with(fake_path)
        self.assertIn("avviato con successo", result)

    @patch('core.tools._open_path')
    @patch('core.tools._find_executable')
    def test_launch_program_not_found(self, mock_find, mock_open):
        """Tests that launch_program returns an error if the executable is not found."""
        fake_program = "notfound.exe"
        
        mock_find.return_value = None
        result = tool_launch_program(fake_program)

        mock_find.assert_called_once_with(fake_program)
        mock_open.assert_not_called()
        self.assertIn("Programma 'notfound.exe' non trovato", result)

if __name__ == '__main__':
    unittest.main()
