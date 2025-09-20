import requests
import concurrent.futures
import functools
import time
import os
import geoip2.database
import json

boolmindmax = False
mindmaxfilepath = "C:/ServerFinder/GeoLite2-Country.mmdb"
mindmaxpath = "C:/ServerFinder/"
mindmaxfetchlink = "https://drive.usercontent.google.com/download?id=1hyZmPjGCzDixKY6HYzFPhoxodl29Elkm&export=download&authuser=0"
logofetch = "https://drive.usercontent.google.com/download?id=19XHw7nCHMRA47gbpAIwwCVzOtKraDjt5&export=download&authuser=0"
soundfetch = "https://drive.usercontent.google.com/u/0/uc?id=1nEPIWSwsZu6d8GKLOcR_VKWPyIPUGjSo&export=download&"
def mindmax_setup():
    global boolmindmax
    if not boolmindmax:
        try:
            if not os.path.exists(mindmaxfilepath):
                print("GeoLite2 database not found. Attempting download...")
                os.makedirs(mindmaxpath, exist_ok=True)
                filename = "GeoLite2-Country.mmdb"
                download_target_path = os.path.join(mindmaxpath, filename)

                print(f"Downloading to: {download_target_path}")
                response = requests.get(mindmaxfetchlink, stream=True, timeout=30)
                response.raise_for_status()
                with open(download_target_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                boolmindmax = True
                print("Downloaded GeoLite2 database successfully.")
            else:
                boolmindmax = True
                print("GeoLite2 database exists.")
        except requests.exceptions.RequestException as e:
            print(f"GeoLite2 download failed due to network error: {e}")
            return False
        except Exception as e:
            return(f"GeoLite2 setup failed because of: {e}")
            return False
    return boolmindmax

def mindmax_lookup(serverip: str) -> dict or None:
    if not boolmindmax or not os.path.exists(mindmaxfilepath):
        print("GeoLite2 database not setup or found.")
        return None

    try:
        with geoip2.database.Reader(mindmaxfilepath) as reader:
            response = reader.country(serverip)
            country_code = response.country.iso_code
            return {
                "country_code": country_code
            }
    except geoip2.errors.AddressNotFoundError:
        return None
    except Exception as e:
        print(f"GeoLite2  failed for {serverip} because of {e}")
        return None

def down_icon():
    try:
        os.chdir("C:/ServerFinder/")
        filename = "logo.ico"
        download_target_path = os.path.join(mindmaxpath, filename)
        response = requests.get(logofetch, stream=True, timeout=30)
        response.raise_for_status()
        with open(download_target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return "Downloaded logo successfully."
    except Exception as e:
        return"Failed to download logo"

def down_sound():
    try:
        os.chdir("C:/ServerFinder/")
        filename = "ding.mp3"
        download_target_path = os.path.join(mindmaxpath, filename)
        response = requests.get(soundfetch, stream=True, timeout=30)
        response.raise_for_status()
        with open(download_target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return "Downloaded logo successfully."
    except Exception as e:
        return"Failed to download logo"


def fetch_serverid(place_id: int) -> list[str]:
    fetchurl = f"https://games.roblox.com/v1/games/{place_id}/servers/public"
    params = {
        "excludeFullGames": True,
        "sortOrder": 2,
        "limit": 50,
    }
    try:
        serverid_response = requests.get(fetchurl, params=params, timeout=10)
        serverid_response.raise_for_status()
        serverid_data = serverid_response.json()
        server_data = serverid_data.get('data', [])
        if not server_data:
            print(f"No  server data in response for place_id.")
            return []
        exctracted_ids = [ids["id"] for ids in server_data]
        return exctracted_ids
    except requests.exceptions.RequestException as e:
        print(f"Rate Limited fetching server IDs for place_id")
        return []
    except Exception as e:
        print(f"exception fetching server IDs for place_id")
        return []
def req_server_data(place_id: int, gameid: str, rblxtoken: str) -> dict or None:
    geturl = "https://gamejoin.roblox.com/v1/join-game-instance"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Roblox/WinInet",
    }
    cookies = {
        ".ROBLOSECURITY": rblxtoken
    }
    payload = {
        "placeId": place_id,
        "gameId": gameid
    }

    location_data = {"country_code": "Unknown"}

    try:
        getresponse = requests.post(geturl, headers=headers, json=payload, cookies=cookies, timeout=10)
        getresponse.raise_for_status()
        response = getresponse.json()

        joinscript = response.get("joinScript")

        if joinscript:
            server_ip = None

            if 'UdmuxEndpoints' in joinscript and joinscript['UdmuxEndpoints']:
                server_ip = joinscript['UdmuxEndpoints'][0]['Address']
            elif 'MachineAddress' in joinscript:
                server_ip = joinscript['MachineAddress']

            if not server_ip:
                print(f"No server IP found in joinScript for Game ID: {gameid}.")
                return None

            if boolmindmax:
                location_result = mindmax_lookup(server_ip)
                if location_result:
                    location_data = location_result
                else:
                    print(f"Could not get detailed location for {server_ip} (Game ID: {gameid}) via GeoLite2. Using default.")

            return {
                "gameid": gameid,
                "location_data": location_data
            }
        else:
            roblox_message = response.get("message", "No specific message from Roblox.")
            print(
                f"No joinScript found for Game ID: {gameid}. Roblox message: {roblox_message}. Full response: {response}")
            return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error for Game ID {gameid}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network/Request Error for Game ID {gameid}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(
            f"JSON Error for Game ID {gameid}")
        return None
    except Exception as e:
        print(f" Error for Game ID {gameid}: {e}")
        return None
def sorting_threading(place_id: int, gameidlist: list[str], rblxtoken: str) -> list[dict]:
    if not gameidlist:
        print("No game IDs provided for sorting_threading.")
        time.sleep(10)
        return []
    start = time.time()

    def threading():
        threading_result = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            task = functools.partial(req_server_data, place_id, rblxtoken=rblxtoken)

            futures_map = {executor.submit(task, gameid): gameid for gameid in gameidlist}

            for future in concurrent.futures.as_completed(futures_map):
                original_gameid = futures_map[future]
                try:
                    server_data_dict = future.result()

                    if server_data_dict and isinstance(server_data_dict,dict) and 'gameid' in server_data_dict and 'location_data' in server_data_dict:
                        threading_result.append(server_data_dict)
                    else:
                        print(
                            f"  Invalid or missing data for game ID {original_gameid}.")
                except Exception as e:
                    print(f"  Exception in processing for game ID {original_gameid}: {e}")
        return threading_result

    results = threading()
    end = time.time()
    print(f"Processed: {len(results)} servers in {end - start:.2f} seconds.")
    return results

def main(cookie,PlaceID,filter):
    cookietemp = cookie
    place_id_input = PlaceID

    if not mindmax_setup():
        print("GeoLite2 setup failed. Location lookups will not work.")
        return False
    def search():
        gameid = fetch_serverid(place_id_input)

        final_servers = sorting_threading(place_id_input, gameid, cookietemp)

        found_filtered_servers = False
        if final_servers:
            for server in final_servers:
                id = server.get('gameid', 'N/A')
                location_info = server.get('location_data', {})
                country_code = location_info.get('country_code', 'N/A')

                if country_code in filter:
                    text = f"\n--- {country_code} Server ---"
                    base_share_url = "\nhttps://oqarshi.github.io/Invite/"
                    share_link = f"{base_share_url}?placeid={place_id_input}&serverid={id}"
                    found_filtered_servers = True
                    print(share_link)
                    link = text + share_link
                    return link

        if not found_filtered_servers:
            print(f"No servers found in {filter}.")
            print("Searching again in 10 seconds...")
            time.sleep(10)
            return search()
    returned = search()
    return returned