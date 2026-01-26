SOURCE_DIR_URL = "https://raw.githubusercontent.com/Ninjago77/scaffoldmc/refs/heads/main/" # + "/scaffoldmc.py", etc....
JSON_SETTINGS_FILE_PATH = "scaffoldmc_settings.json"
######################## DO NOT EDIT AFTER THIS LINE ########################
from urllib.request import urlopen, Request
import json, os

import urllib

def download_purpur(version: str = "latest"):
    if version == "latest":
        with urllib.request.urlopen("https://api.purpurmc.org/v2/purpur") as response:
            data = json.loads(response.read().decode())
        latest_mc_version = data['versions'][-1]
        download_url = f"https://api.purpurmc.org/v2/purpur/{latest_mc_version}/latest/download"
    else:
        download_url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"

    httprequest = Request(download_url, headers={"Accept": "application/json"})
    with urlopen(httprequest) as response:
        with open("./server.jar","wb") as file:
            file.write(response.read())

def download_paper(version: str = "latest"):
    if version == "latest":
        with urllib.request.urlopen("https://api.papermc.io/v2/projects/paper") as response:
            data = json.loads(response.read().decode())
        version = data['versions'][-1]

    httprequest = Request(f"https://api.papermc.io/v2/projects/paper/versions/{version}", headers={"Accept": "application/json"})
    with urlopen(httprequest) as response:
        data = json.loads(response.read().decode())
    
    latest_build = data['builds'][-1]
    filename = f"paper-{version}-{latest_build}.jar"

    httprequest = Request(f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/{filename}", headers={"Accept": "application/json"})
    with urlopen(httprequest) as response:
        with open("./server.jar","wb") as file:
            file.write(response.read())

def download_fabric(version: str = "latest"):
    if version == "latest":
        httprequest = Request("https://meta.fabricmc.net/v2/versions/game", headers={"Accept": "application/json"})
        with urlopen(httprequest) as response:
            data = json.loads(response.read().decode())
        for entry in data:
            if entry['stable']:
                version = entry['version']
                break

    httprequest = Request(f"https://meta.fabricmc.net/v2/versions/loader/{version}", headers={"Accept": "application/json"})
    with urlopen(httprequest) as response:
        data = json.loads(response.read().decode())
    latest_loader = data[0]['loader']['version']

    httprequest = Request(f"https://meta.fabricmc.net/v2/versions/installer", headers={"Accept": "application/json"})

    with urlopen(httprequest) as response:
        data = json.loads(response.read().decode())
    latest_installer = data[0]['version']

    download_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{latest_loader}/{latest_installer}/server/jar"

    httprequest = Request(download_url, headers={"Accept": "application/json"})
    with urlopen(httprequest) as response:
        with open("./server.jar","wb") as file:
            file.write(response.read())

LOADER_TYPES = {
    "purpur": {"dir":"./plugins",  "func": download_purpur},
    "paper": {"dir":"./plugins", "func": download_paper},
    "fabric": {"dir":"./mods", "func": download_fabric},
}


with open(JSON_SETTINGS_FILE_PATH,"r") as settings_file:
    SETTINGS = json.load(settings_file)

if SETTINGS["self-update"]:
    httprequest = Request(SOURCE_DIR_URL.strip("/") + "/scaffoldmc.py", headers={"Accept": "application/json"})

    with urlopen(httprequest) as response:
        if not response.status == 200:
            raise ConnectionRefusedError("Response Status is not '200' (OK), it is "+response.status)
        with open(__file__,"r+") as file:
            line1 = file.readline()
            line2 = file.readline()
        with open(__file__,"w+") as file:
            file.write(
                line1 + line2 +
                response.read().decode().split("\n",2)[2]            
            )

os.makedirs(SETTINGS["directory"], exist_ok=True)
os.chdir(SETTINGS["directory"])

if SETTINGS["update-server"]:
    LOADER_TYPES[SETTINGS["platform"]]["func"](SETTINGS["version"])

        