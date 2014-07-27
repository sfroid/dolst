"""
Throwaway file for playing with the Popen command
"""

from subprocess import Popen, PIPE
from os.path import dirname, abspath, join


OUTPUT = Popen(["python", "tests/test_pep8_lint_flakes.py",
                join(dirname(dirname(abspath(__file__))), "main_app.py")],
               stdout=PIPE).communicate()[0]

print OUTPUT
