import subprocess
import sys
import re

REPO_ROOT = sys.path[0]

def run_cmd(args):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)

def test_generate_and_fakeout():
    result = run_cmd([sys.executable, 'generate_key.py'])
    assert 'Generated Key:' in result.stdout
    match = re.search(r'Generated Key:\s*(\S+)', result.stdout)
    assert match, 'key not found'
    key = match.group(1)
    fake = run_cmd([sys.executable, 'self-destruct.py', '--fakeout', '-k', key])
    assert 'Debugging..' in fake.stdout
