import logging
import time

import demo
import pytest


# @pytest.mark.parametrize("test_data2", [1,1,1])
def test_square(test_data):
    logging.info("This is a test")
    time.sleep(test_data.get("input"))
    result = demo.t_square(test_data.get("input"))
    assert  result == test_data.get("result"), f"Expected: {test_data.get('result')}, Actual: {result}"



# def test_square_b(input_test):
#     assert demo.t_square(input_test.b()) == 25
