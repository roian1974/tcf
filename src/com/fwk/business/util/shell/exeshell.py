import subprocess

def exeshell(cmdstr) :
    # subprocess.call('ls -al', shell=True)
    subprocess.call(cmdstr, shell=True)

def rtnshell(cmdstr) :
    result = subprocess.check_output(cmdstr, shell=True)
    if result == 'AAA':
        print
        "123"
    elif result == 'BBB':
        print
        "456"
