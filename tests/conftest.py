import pytest
import time
from subprocess import Popen


@pytest.fixture(scope="session", autouse=True)
def app():
    port = 9507
    cmd = f"uv run streamlit run main.py --server.port {port} --server.headless true"
    process = Popen(cmd.split())
    time.sleep(3)
    yield
    process.terminate()
