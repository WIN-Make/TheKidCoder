import time
import webbrowser

print("Wellcome to PyNetBomb")
time.sleep(1)
Url=input("Enter Url to bomb:")

while True:
   webbrowser.open(Url)
