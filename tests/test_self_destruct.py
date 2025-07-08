import subprocess
import sys
import re


def get_generated_key():
    proc = subprocess.run([sys.executable, 'generate_key.py'], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    match = re.search(r"Generated Key: (.+)", proc.stdout)
    assert match, "Key not found in output"
    return match.group(1).strip()


def test_generated_key_is_valid():
    key = get_generated_key()
    proc = subprocess.run([sys.executable, 'self-destruct.py', '-k', key, '-f'], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert 'destroy: False' in proc.stdout
    assert 'wrong_secret: False' in proc.stdout
