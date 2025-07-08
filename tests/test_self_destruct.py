import subprocess
import sys
from pathlib import Path


def test_malformed_key_exit():
    script = Path(__file__).resolve().parents[1] / "self-destruct.py"
    result = subprocess.run([sys.executable, str(script), "-k", "invalidkey"], capture_output=True)
    assert result.returncode == 1
    assert b"There is a problem with the key" in result.stdout
