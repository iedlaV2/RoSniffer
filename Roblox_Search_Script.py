import requests
import concurrent.futures
import functools
import time
import os
import geoip2.database
import json
import webbrowser

boolmindmax = False
mindmaxfetchlink = "https://drive.usercontent.google.com/download?id=1hyZmPjGCzDixKY6HYzFPhoxodl29Elkm&export=download&authuser=0"
logofetch = "https://github.com/iedlaV2/Rosniffer-Downloads/releases/download/v0/logo.ico"
soundfetch = "https://github.com/iedlaV2/Rosniffer-Downloads/releases/download/v0/ding.mp3"

def down_icon(target_full_path):
    try:
        response = requests.get(logofetch, stream=True, timeout=30)
        response.raise_for_status()
        with open(target_full_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"Downloaded logo successfully to {target_full_path}."
    except requests.exceptions.RequestException as e:
        return f"Failed to save logo to {target_full_path}: {e}"
    except Exception as e:
        return f"An unexpected error occurred during logo download: {e}"
def down_sound(target_full_path):
    try:
        response = requests.get(soundfetch, stream=True, timeout=30)
        response.raise_for_status()
        with open(target_full_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"Downloaded sound successfully to {target_full_path}."
    except requests.exceptions.RequestException as e:
        return f"Failed to download sound from {soundfetch}: {e}"
    except Exception as e:
        return f"An unexpected error occurred during sound download: {e}"
def down_db(mindmax_target_full_path):
    global mindmax_path
    mindmax_path = mindmax_target_full_path
    try:
        response = requests.get(mindmaxfetchlink, stream=True, timeout=30)
        response.raise_for_status()
        with open(mindmax_target_full_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"Downloaded sound successfully to {mindmax_target_full_path}."
    except requests.exceptions.RequestException as e:
        return f"Failed to download sound from {soundfetch}: {e}"
    except Exception as e:
        return f"An unexpected error occurred during sound download: {e}"
def mindmax_lookup(serverip: str) -> dict or None:
    if not boolmindmax or not os.path.exists(mindmax_path):
        print("GeoLite2 database not setup or found.")
        return None

    try:
        with geoip2.database.Reader(mindmax_path) as reader:
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
                    text = f"--- {country_code} Server ---"
                    base_share_url = "\nhttps://iedlav2.github.io/RoSniffer-Forwarder/"
                    share_link = f"{base_share_url}?placeid={place_id_input}&serverid={id}"
                    found_filtered_servers = True
                    print(share_link)
                    link = text + share_link
                    webbrowser.open(link)
                    return link

        if not found_filtered_servers:
            print(f"No servers found in {filter}.")
            print("Searching again in 10 seconds...")
            time.sleep(10)
            return search()
    returned = search()
    return returned