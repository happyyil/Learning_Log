import webbrowser
import sys

url = "http://127.0.0.1:8000"
url_global = "http://ll.he-ying.top"

if "global" in sys.argv:
    webbrowser.open_new(url_global)
else:
    webbrowser.open_new(url)
