import os
import sys
import json
import pywinctl as pwc

def printHelp():
  print("""relocate.py: Relocate a specified window.
             Load relocate-conf.json file located same location as this file.
Options
  help - Print this.
  info - Display specified window info without relocate.
  apps - Display all apps and windows titles.
  conf - Print example config file.
          Run this to use it. 'python3 relocation.py conf > relocate-conf.json'""")

def printConf():
  print("""{
  "app_name": "",
  "title": "",
  "move_to": {
    "x": 0,
    "y": 0
  },
  "new_size": {
    "w": 1000,
    "h": 1000
  }
}
""")

def printApps():
  apps = pwc.getAllAppsWindowsTitles()
  for a in apps:
    print(f"[{a}]", file=sys.stderr)
    for title in apps[a]:
      print(f"  \"{title}\"", file=sys.stderr)
    if len(apps[a]) < 1:
      print(f"  No entries", file=sys.stderr)

def printInfo(x, y, w, h):
  print(f"""[Window info]
x: {x}
y: {y}
w: {w}
h: {h}
""")

def main():
  arg = ""
  appName = ""
  title = ""
  x = 0
  y = 0
  w = 1000
  h = 1000

  if ( 2 < len(sys.argv)):
    print(f"too many arguments", file=sys.stderr)
    printHelp()
    os._exit(1)
  elif (len(sys.argv) == 2):
    arg = sys.argv[1]

  conf_path = f"{os.path.dirname(os.path.abspath(__file__))}/relocate-conf.json"

  if arg in ["", "help", "conf", "apps", "info"]:
    if (arg == "help"):
      printHelp()
      os._exit(0)
    if (arg == "conf"):
      printConf()
      os._exit(0)
    if (arg == "apps"):
      printApps()
      os._exit(0)
  else:
    conf_path = arg

  # Load config
  with open(conf_path) as f:
    conf = json.load(f)
    appName = conf["app_name"]
    title = conf["title"]
    x = conf["move_to"]["x"]
    y = conf["move_to"]["y"]
    w = conf["new_size"]["w"]
    h = conf["new_size"]["h"]

  if (appName == ""):
    print(f"cannot parse config: \"{appName}\", \"{title}\" \"{x}\", \"{y}\"", file=sys.stderr)
    raise

  targetAppTitles = pwc.getAllAppsWindowsTitles()[appName]

  # Check app, title
  if (len(targetAppTitles) < 1):
    print(f"app has no title", file=sys.stderr)
    printApps()
    raise

  if title == "":
    if (len(targetAppTitles) == 1):
      title = targetAppTitles[0]
    else:
      print(f"app has {len(targetAppTitles)} titles", file=sys.stderr)
      printApps()
      raise

  # Move window to location
  targetWindow = pwc.getWindowsWithTitle(title=title)
  if (len(targetWindow) == 0):
    print(f"title not found: {title}", file=sys.stderr)
    printApps()
    raise

  t = targetWindow[0]

  if (arg != "info"):
    t.moveTo(x, y)
    t.resizeTo(w, h)
    print(f"Target was moved")

  printInfo(t.position.x, t.position.y, t.size.width, t.size.height)

if __name__ == "__main__":
    main()
  # try:
  #   main()
  # except:
  #   os._exit(1)
