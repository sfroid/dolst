"""
Throwaway file for playing with the Popen command
"""

from subprocess import Popen, PIPE

OUTPUT = Popen(["python", "tests/test_pep8_lint_flakes.py",
                "/home/nagarajan/programs/dolst/gitrepo/main_app.py"],
               stdout=PIPE).communicate()[0]

print OUTPUT
