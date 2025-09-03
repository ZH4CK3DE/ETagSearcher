import requests
from colorama import *
import time 

init(autoreset=True)

# api 
API = "https://api.ransomware.live/v2/groups"

# output
output = "data.txt"

ascii_art = r"""
                                                                                                
,------.,--------.                   ,---.                              ,--.                    
|  .---''--.  .--',--,--. ,---.     '   .-'  ,---.  ,--,--.,--.--. ,---.|  ,---.  ,---. ,--.--. 
|  `--,    |  |  ' ,-.  || .-. |    `.  `-. | .-. :' ,-.  ||  .--'| .--'|  .-.  || .-. :|  .--' 
|  `---.   |  |  \ '-'  |' '-' '    .-'    |\   --.\ '-'  ||  |   \ `--.|  | |  |\   --.|  |    
`------'   `--'   `--`--'.`-  /     `-----'  `----' `--`--'`--'    `---'`--' `--' `----'`--'    
                         `---'                                                                                                            

    Ransomware Groups ETag Searcher (via ransomware.live API)
    By: github.com/ZH4CK3DE
"""

def ransomwaregroups():
    try:
        r = requests.get(API, timeout=15)
        r.raise_for_status()  # will raise an exception if not 200
        return r.json()
    except Exception as e:
        print(Fore.RED + f"[ERROR] API request failed: {e}")
        return []

def main():
    print(Fore.RED + ascii_art + Style.RESET_ALL)
    print(Fore.YELLOW + "[INFO] Fetching groups...\n")
    time.sleep(3)
    groups = ransomwaregroups()
    if not groups:
        print(Fore.RED + "[ERROR] No data received.")
        return

    with open(output, "w", encoding="utf-8") as f:
        f.write("GROUP | WEBSITE | ETAG\n\n")
        for group in groups:
            name = group.get("name", "n/a")
            for loc in group.get("locations", []):
                fqdn = loc.get("fqdn", "n/a")
                # headers may or may not include etag --> skip if missing
                etag = loc.get("http", {}).get("headers", {}).get("etag")
                if etag:
                    line = f"{name} | {fqdn} | {etag}"
                    print(Fore.CYAN + "[OK] " + Fore.WHITE + line)
                    f.write(line + "\n")

    print(Fore.GREEN + f"\n[DONE] Results saved to {output}")

if __name__ == "__main__":
    main()
