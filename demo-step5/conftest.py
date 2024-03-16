import json

import pytest
import pytest_html


# Modify the title of HTML report
def pytest_html_report_title(report):
    ''' modifying the title  of html report'''
    report.title = "TechTalk test report"

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    '''data from the output of pytest gets processed here
     and are passed to pytest_html_results_table_row'''
    outcome = yield
    # this is the output that is seen end of test case
    report = outcome.get_result()
    report.test_name = ""
    report.test_name = item.originalname

# Generate test cases dynamically
def pytest_generate_tests(metafunc):
    # Extract the name of the fixture
    func_name = metafunc.fixturenames[0]
    metafunc.parametrize(func_name, metafunc.config.test_data)

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend(["<p>these are example test run for the TechTalks session<p>"])
    summary.extend(["<h2>Summary1</h2>",  "<h2>Summary2</h2>", "<h2>Summary3</h2>", "<h2>Summary4<h2>"])
    postfix.extend(["<p>more data</p>"])

# Add custom command-line options
def pytest_addoption(parser):
    parser.addoption("--test_file", action="store",
                     help="path to the devices list txt")


@ pytest.hookimpl(trylast=True)
def pytest_configure(config):
    test_file_path = config.getoption("--test_file", default=None)
    # test_neds = config.getoption("--test_neds", default=None)
    # print(f"Test file path: {test_file_path}")
    config.test_data = load_data(test_file_path)


def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data




# Hook to modify the test item collection process
def pytest_collection_modifyitems(config, items):
    for item in items:
        # Check if the test item is a function
        if item.nodeid.startswith("toto_") and item.cls is None:
            file_name, _, function_name = item.nodeid.partition("::")
            params = item.callspec.params
            # Convert parameters to a string and add it to the test description
            param_string = ", ".join(f"{value}" for param, value in params.items())
            item._nodeid = f"Test: file {file_name} : funtion {function_name} : parameters {param_string}"
