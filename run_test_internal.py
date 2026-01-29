import unittest
import sys

def run_tests():
    with open('internal_test_result.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        loader = unittest.TestLoader()
        suite = loader.discover('tests', pattern='test_prompt_injection.py')
        result = runner.run(suite)
        
    if result.wasSuccessful():
        print("TEST PASSED")
    else:
        print("TEST FAILED")

if __name__ == '__main__':
    run_tests()
