import unittest
import os

def main():
    test_dir = os.path.dirname(__file__)  
    
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern="Test*.py")  

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print(f"Tests failed: {len(result.failures) + len(result.errors)}")
        for failure in result.failures + result.errors:
            print(failure[1])

if __name__ == "__main__":
    main()
