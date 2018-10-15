import subprocess

subprocess.check_call(['service', 'plexmediaserver', 'stop'])
subprocess.check_call(['service', 'plexmediaserver', 'start'])