SOURCE_DIR_URL = "https://raw.githubusercontent.com/Ninjago77/scaffoldmc/refs/heads/main/" # + "/scaffoldmc.py", etc....
JSON_SETTINGS_PATH = ""
######################## DO NOT EDIT AFTER THIS LINE ########################
from urllib.request import urlopen, Request

httprequest = Request(SOURCE_DIR_URL.strip("/") + "/scaffoldmc.py", headers={"Accept": "application/json"})

with urlopen(httprequest) as response:
    if not response.status == 200:
        raise ConnectionRefusedError("Response Status is not '200' (OK), it is "+response.status)
    with open(__file__,"r+") as file:
        file.write(
            file.readline() + "\n" +
            file.readline() + "\n" +
            response.read().decode().split("\n",2)[2]            
        )
        