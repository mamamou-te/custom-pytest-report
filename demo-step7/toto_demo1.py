import logging
import time

import demo
import pytest


def test_square(test_data):
    logging.info("This is a test")
    # This will influence the test duration and will be shown in the html report file
    if test_data.get('result') not in ["skip", "Expected fail"]:    
        time.sleep(test_data.get("input"))
    result = demo.t_square(test_data.get("input"))
    if test_data.get('result') == "skip":
        pytest.skip("unsupported!")
    elif test_data.get('result') == "Expected fail":
        pytest.xfail("Expected fail")
    else:
        assert  result == test_data.get("result"), f"Expected: {test_data.get('result')}, Actual: {result}"
        
    
    
    
    
    