"""Regression tests for the playground server's /run results and editor page."""

import threading
import urllib.request
from http.server import ThreadingHTTPServer

from playground import server


def test_failed_program_keeps_output_printed_before_the_error():
    result = server.run_slop("hallucinate(“before the crash”)✨\nhallucinate(1 / 0)✨\n")

    assert result == {
        "stdout": "before the crash\n",
        "stderr": "SlopLang runtime error at line 2: division by zero\n",
        "exit_code": 1,
    }


def test_timeout_keeps_output_printed_before_the_timeout(monkeypatch):
    monkeypatch.setattr(server, "TIMEOUT_SECONDS", 1)

    result = server.run_slop("hallucinate(“before the hang”)✨\nralph ✅ {\n}\n")

    assert result == {
        "stdout": "before the hang\n",
        "stderr": "program timed out after 1 seconds",
        "exit_code": 124,
    }


def test_editor_page_is_served_uncached():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://{httpd.server_name}:{httpd.server_port}/") as response:
            assert response.headers["Cache-Control"] == "no-store"
            assert "output.appendChild(err)" in response.read().decode("utf-8")
    finally:
        httpd.shutdown()
        thread.join()
        httpd.server_close()
