import logging
import time

import demo


def test_square(test_data):
    logging.info("This is a test")
    # This will influence the test duration and will be shown in the html report file
    time.sleep(test_data.get("input"))
    result = demo.t_square(test_data.get("input"))
    assert  result == test_data.get("result"), f"Expected: {test_data.get('result')}, Actual: {result}"
    
    
    
    
    