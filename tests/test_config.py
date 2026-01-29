import sys
import os
import unittest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import OLLAMA_URL, MODEL_NAME

class TestConfig(unittest.TestCase):
    def test_config_defaults(self):
        # Assuming .env might not be present or might have defaults
        self.assertTrue(OLLAMA_URL.startswith("http"))
        self.assertTrue(len(MODEL_NAME) > 0)

if __name__ == '__main__':
    unittest.main()
