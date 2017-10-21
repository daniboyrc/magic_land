import sys
from io import BytesIO
from subprocess import Popen
import subprocess
"""
print PIPE
buff = BytesIO()
sys.stdout = buff

nome = raw_input('daniel: ')

print 'fdsa'

arq = open('arq.txt', 'w')
arq.write(buff.getvalue())
"""

process = Popen('python teste.py', stdout=subprocess.PIPE, shell=True)

print process.communicate()