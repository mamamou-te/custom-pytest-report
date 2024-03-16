import json

import pytest
import pytest_html

# import test_logic


# Modify the title of HTML report
def pytest_html_report_title(report):
    ''' modifying the title  of html report'''
    report.title = "TechTalk test report"

# Additinal summary prefix
# def pytest_html_results_summary(prefix, summary, postfix):
#     summary.extend(["<h2>Summary 2</h2>","<h2>Summary 3</h2>"])
#     prefix.extend(["<p>foo: bar</p>"])
#     postfix.extend(["<p>foo: bar</p>"])

def pytest_html_results_table_header(cells):
    ''' meta programming to modify header of the result'''
#     # removing old table headers
    # del cells[3]
    # del cells[2]
    # del cells[3]
    # adding new headers
    print(f"cells {dir(cells)}")
    # cells.insert(4, '<th>Devices</th>')
    # cells.insert(5, '</th>Testcase</th>')
    # cells.insert(6, '</th>Info</th>')
    # cells.append('<th class="sortable time" data-column-type="time">Time</th>')
    # cells.insert(7, html.th('Time', class_='sortable time', col='time'))
    # cells.pop()

def pytest_html_results_table_row(report, cells):
    # cells.insert(4, f"<td>tests</td>")
    # del cells[0]
    # cells[2] = f"<td>{report.duration}</td>"
    cells[1] =  f"<td>Test name: <b>{report.test_name}</b><br> Test input value: <b>{report.test_input}</b> <br> Test expected output <b>{report.test_output}</b> <td>"
    
    
    print(dir(report))
    
    # cells.pop()
    # cells.insert(1, f'<td class="col-time">{datetime.utcnow()}</td>')

def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(f"<div class='empty log'>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br>No log output captured. <br> {report.longreprtext} </div>")
    else:
        del data[:]
        data.append(f"<div class_='log'>Logs here <br> {report.longreprtext}</div>")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    '''data from the output of pytest gets processed here
     and are passed to pytest_html_results_table_row'''
    outcome = yield
    # this is the output that is seen end of test case
    report = outcome.get_result()
    report.test_name = ""
    print(f"Toto: {dir(item)}")
    print(f"Toto2: {item.name}")
    print(f"Toto3: {item.nodeid}")
    print(f"Toto4: {item.originalname}")
    print(f"Toto5: {item.path}")
    print(f"Toto5: {item.path}")
    print(f"Toto6: {item.funcargs.values()}")
    print(f"Report element {dir(report)}")
    report.test_name = item.originalname
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        # print(f"tototototot {dir(pytest_html.extras.extra)}")
        extras.append(pytest_html.extras.url("http://www.example.com/"))
        xfail = hasattr(report, "wasxfail")
        # if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
        extras.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        # extras.append(1)
    print(dir(f"okok {item.funcargs}"))
    for v in item.funcargs.values():
        extras.append(pytest_html.extras.json(v))
        print(f"test parameter: {v}")
        report.test_input = v.get("input")
        report.test_output = v.get("result")
    report.extras = extras

# Generate test cases dynamically
def pytest_generate_tests(metafunc):
    print("Entering pytest_generate_tests")
    # Extract the name of the fixture
    func_name = metafunc.fixturenames[0]
    print(  # pylint: disable=W1203
        f"{metafunc.config.test_data}")  # pylint: disable=W1203

    metafunc.parametrize(func_name, metafunc.config.test_data)

def input_output(element):
    return [element]
# Add custom command-line options
def pytest_addoption(parser):
    parser.addoption("--test_file", action="store",
                     help="path to the devices list txt")
#     parser.addoption("--test_neds", action="store",
                    #  help="String: list of neds used during this test")
@pytest.fixture
def test_file(request):
    return request.config.getoption("--test_file")

@ pytest.hookimpl(trylast=True)
def pytest_configure(config):
    test_file_path = config.getoption("--test_file", default=None)
    # test_neds = config.getoption("--test_neds", default=None)
    print(f"Test file path: {test_file_path}")
    config.test_data = load_data(test_file_path)


def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data
