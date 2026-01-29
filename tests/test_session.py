import sys
import os
import unittest
import asyncio
import logging
from unittest.mock import patch, MagicMock, AsyncMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.session import Session

class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(logging.getLogger("seeker_cli"))

    def test_init(self):
        self.assertEqual(len(self.session.history), 0)

    def test_handle_local_command_help(self):
        result = self.session.handle_local_command("/help")
        self.assertIsNone(result)

    def test_handle_local_command_clear(self):
        self.session.history.append({"role": "user", "content": "test"})
        self.session.handle_local_command("/clear")
        self.assertEqual(len(self.session.history), 0)

    @patch('core.session.call_ollama', new_callable=AsyncMock)
    def test_process_input_chat(self, mock_call_ollama):
        mock_call_ollama.return_value = '{"action": "chat", "args": {"message": "Hello"}, "thought": "Greeting"}'
        with patch('core.session.classify_request', MagicMock(return_value="general_chat")):
            asyncio.run(self.session.process_input("Hi"))

        self.assertTrue(any(m['content'] == 'Hi' for m in self.session.history))
        self.assertTrue(any('"action": "chat"' in m['content'] for m in self.session.history))

if __name__ == '__main__':
    unittest.main()
