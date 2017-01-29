#Checkout Python and Arduino files from repo.
# 2017-01-29 Auth: Dylan

import subprocess

repo = 'https://github.com/Brendoncamm/SYP/trunk/'

folders = [repo + 'Python',
           repo + 'Arduino']

try:
    for entry in range(0,len(folders)):
        subprocess.call(['svn', 'checkout', folders[entry]], cwd = '/home/pi/Documents/')
except FileNotFoundError:
    subprocess.call(['sudo','apt-get','install','subversion'])
    subprocess.call(['python3', 'checkout.py'])
