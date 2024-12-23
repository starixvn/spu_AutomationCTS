import pytest
import os
import json
import time

log_init = False

def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='local'
    )

# @pytest.fixture
def pytest_configure(config):
    pytest.env = config.getoption('env')

@pytest.fixture(autouse=True)
def measure_duration(request):
    global log_init
    log_file_path = os.path.join('test_results', 'durations.json')
    if not log_init:
        with open(log_file_path, "w") as f:
            json.dump({"Testcases": []}, f)
        log_init = True
    start_time = time.time()
    yield
    duration = time.time() - start_time
    test_file_name = os.path.basename(request.node.fspath)
    log_entry = {
        "TestSuites": test_file_name,
        "Testcase": request.node.name,
        "Duration": f"{duration:.2f}"
    }
    with open(log_file_path, "r+") as f:
        data = json.load(f)
        data["Testcases"].append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)