import sys
import os
import subprocess
import re
import time


def AppName(d_name: str):
    # print(d_name)
    login = os.getlogin()
    app_dirs = ['/usr/share/applications/', '/home/{}/.local/share/applications/'.format(login)]
    name_exists = False
    for path in app_dirs:
        find_desktop = subprocess.Popen('cd {0}\nls | grep {1}'.format(path, d_name), stdout=subprocess.PIPE, shell=True)
        stdout1, stderr1 = find_desktop.communicate()
        if not name_exists:
            if stdout1:
                name = stdout1.decode('utf-8').split()[0]
                name_exists = True
                find_name = subprocess.Popen('cd {0}\nxargs -0 -a {1}'.format(path, name), stdout=subprocess.PIPE, shell=True)
                stdout2, stderr2 = find_name.communicate()
                args = stdout2.decode('utf-8')
                args_after_name = args[args.find('Name=') + 5:]
                args_with_end = args_after_name.split('=')[0]
                name = ' '.join(args_with_end.split()[:-1])
        else:
            break
    if not name_exists:
        return d_name.capitalize()
    return name


def get_active_app():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    m = re.search(br'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None
    match = re.search(br"WM_CLASS\(\w+\) = (.+)", stdout)
    if match != None:
        some_name = match.groups()[0].decode('utf-8').split(',')[0].strip('"').lower().split()
        some_name = '-'.join(some_name)
        return AppName(some_name)
    return None


if __name__ == "__main__":
    while True:
        app = get_active_app()
        time.sleep(1)