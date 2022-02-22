import sys
from tempfile import mkdtemp
import venv
import subprocess
import shutil

argv = sys.argv[1:]
tmp_dir = mkdtemp()
print(tmp_dir)
venv.create(tmp_dir, with_pip=True)
pip_path = tmp_dir + "/bin/pip"
subprocess.run([pip_path, "install", "pyfiglet"])
subprocess.run(["python3", "-m", "figdate"] + argv)
shutil.rmtree(tmp_dir)
