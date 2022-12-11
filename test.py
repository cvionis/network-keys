import shlex

print(shlex.split("netsh wlan export profile name={profile_value} folder={cwd}\profile_info key=clear | @echo off"))

