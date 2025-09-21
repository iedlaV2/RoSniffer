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
logofetch = "https://release-assets.githubusercontent.com/github-production-release-asset/1060991946/84699b35-8b74-4bc7-9a79-bf450bf53eeb?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-09-21T03%3A31%3A34Z&rscd=attachment%3B+filename%3Dlogo.ico&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-09-21T02%3A31%3A20Z&ske=2025-09-21T03%3A31%3A34Z&sks=b&skv=2018-11-09&sig=J5jqWULaSivxMasWwBMTI5lF7h3xnqqNOpipnW2C1rc%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc1ODQyMjU1MywibmJmIjoxNzU4NDIyMjUzLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.g_hTahtImk28jVXNO16q3sievdCDeYpuzCs4MouUtiU&response-content-disposition=attachment%3B%20filename%3Dlogo.ico&response-content-type=application%2Foctet-stream"
soundfetch = "https://release-assets.githubusercontent.com/github-production-release-asset/1060991946/5334581c-e634-4610-b603-d139717694d0?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-09-21T03%3A10%3A28Z&rscd=attachment%3B+filename%3Dding.mp3&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-09-21T02%3A09%3A45Z&ske=2025-09-21T03%3A10%3A28Z&sks=b&skv=2018-11-09&sig=XNzjhH4t63fVzbxLMN1ZPhvCyolh6uNqnqGRXFMSy0M%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc1ODQyMjUyMSwibmJmIjoxNzU4NDIyMjIxLCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.7sPdlbiPuYjWQSWBLCUlOZ3DRk2uGPHnWIw9kXmTQ8Y&response-content-disposition=attachment%3B%20filename%3Dding.mp3&response-content-type=application%2Foctet-stream"
fontfetch = "https://release-assets.githubusercontent.com/github-production-release-asset/1060991946/a8bbaac8-193b-4ed0-8205-c939b82347e2?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-09-21T03%3A26%3A06Z&rscd=attachment%3B+filename%3DMuseoSansCyrl.ttf&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-09-21T02%3A25%3A30Z&ske=2025-09-21T03%3A26%3A06Z&sks=b&skv=2018-11-09&sig=DSnkrz8T0Dp2LxYA4NDAqW0ZIJNpmWCPAvEpikvtHO4%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc1ODQyMjU4NSwibmJmIjoxNzU4NDIyMjg1LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.15TMgXdiKkD_Nz8xGzJRLEvIeRebGM8y4mryCGpD3r0&response-content-disposition=attachment%3B%20filename%3DMuseoSansCyrl.ttf&response-content-type=application%2Foctet-stream"
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
def down_font():
    try:
        os.chdir("C:/ServerFinder/")
        filename = "MuseoSansCyrl.ttf"
        download_target_path = os.path.join(mindmaxpath, filename)
        response = requests.get(fontfetch, stream=True, timeout=30)
        response.raise_for_status()
        with open(download_target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return "Downloaded font successfully."
    except Exception as e:
        return"Failed to download font"
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
                    text = f"--- {country_code} Server ---"
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