import unittest
from unittest.mock import patch, Mock
import os
import platform
import asyncio
from core.llm import call_ollama
from core.config import BASE_SPECIALIST_PROMPT

class TestPromptInjection(unittest.TestCase):
    @patch('core.llm.requests.post')
    def test_system_prompt_injection(self, mock_post):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {'message': {'content': '{}'}}
        mock_post.return_value = mock_response

        # Call the function
        asyncio.run(call_ollama([{"role": "user", "content": "test"}], BASE_SPECIALIST_PROMPT, ""))

        # Get the arguments passed to requests.post
        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        messages = payload['messages']
        system_message = messages[0]

        # Verify system message content
        expected_cwd = os.getcwd()
        expected_username = os.getlogin()
        expected_os = platform.system()

        self.assertIn(f"User: {expected_username}", system_message['content'])
        self.assertIn(f"Working Directory: {expected_cwd}", system_message['content'])
        self.assertIn(f"Operating System: {expected_os}", system_message['content'])

if __name__ == '__main__':
    unittest.main()
