"""A tiny web playground: POST source to /run, get stdout, stderr, and an exit code back."""

import json
import subprocess
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PLAYGROUND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PLAYGROUND_DIR.parent
INTERPRETER = PROJECT_DIR / "sloperator.py"
TIMEOUT_SECONDS = 5
DEFAULT_PORT = 8080


def _text(output: str | bytes | None) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")
    return output


def run_slop(source: str) -> dict[str, str | int]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "program.slop"
        path.write_text(source, encoding="utf-8")
        try:
            completed = subprocess.run(
                # Unbuffered, so output printed before a crash or timeout is not stuck in a pipe.
                [sys.executable, "-u", str(INTERPRETER), str(path)],
                capture_output=True,
                encoding="utf-8",
                timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as expired:
            stderr = _text(expired.stderr)
            if stderr and not stderr.endswith("\n"):
                stderr += "\n"
            return {
                "stdout": _text(expired.stdout),
                "stderr": f"{stderr}program timed out after {TIMEOUT_SECONDS} seconds",
                "exit_code": 124,
            }
    return {
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "exit_code": completed.returncode,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = (PLAYGROUND_DIR / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        # Always serve the current editor page so a tab never runs stale JavaScript.
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/run":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_error(400, "request body must be JSON")
            return
        result = run_slop(str(payload.get("source", "")))
        log_path = PROJECT_DIR / "logs" / "runs.log"
        log_path.parent.mkdir(exist_ok=True)
        with log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(result) + "\n")
        body = json.dumps(result).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main(argv: list[str]) -> int:
    port = int(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SlopLang playground running at http://localhost:{port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
