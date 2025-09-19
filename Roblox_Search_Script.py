import requests
import concurrent.futures
import functools
import time
import os
import subprocess
import geoip2.database
import json

cookietemp = "CAEaAhAB.26C98C9BDDADF35973879BB010A2D1A99BB7CD79CD2E41523F0045D30F194B73D2A91D4A7951613120B147943163809EEE9512CAB3828398B5DD786105A74C186C14EF0A4EB03D16B12DCF2A2F13585DF5856DE94563A5E854BE5F9A1346184E633F5A2042B804AD7C3A704B84972D33961E32707B054106C468DFFA3586BF4DD39FCFC251A8AAC74E00EC279E403F736FCCD1B2AB25D82D3F448949FC093E94CDF05D2A882AA5AE74F665B6CB6B0902BBC19A03CE6948EF0086C3DCCC564C4F0BCE29BB9283F665773E6F8CAD3CDB4F20CDE87AE4EA26208DD32C5915357D29EEEED28CE6EE2B91F50413F36D09B27A0EB73888B4580ECFAE2525431CCDB36A0B956E5B385E7B360196673469D2ACCED5F66B33231B3783950DEDBF0ED2B9E99D797F27A79D373D4606990A49506567AC2A6FB03C0BF292204B392F800A4D4F580B5AD946622B970CF7EFBE6EBE5870BC93C88903BB48EC02E764B70826B377B671E61791F49D252B32761EC8BEFDC595BC2DE84B5FDE4FCE76F30D0DE54D8E14EBFB4EDD893D938243CE4F094C58803D10024AD518C1CFFBFA5F0B08A26BEFC724EE839F756B2EF0962D5942CF6AD754104ADF470A93E396D3AEB744528C58AE77B4C8A4734CBAD5B6F148399EF054DF61A2E3B556140A3B39C168D023800798074FCBC0D400AA7CC3F765EBCEB41BFB83E0FEE7AF9DEAB6F7498B7C6E970D0EE1A4C5FF23092C6C648CECD77562D1CFD05E94D8B591BB5013FA83759E6E1B19A41756CEA4DF3E38682ECE7156D2CF5CBE29CACF05F9830BA0110FBC418F7FECAC5D3EEDCC50991607B868C764D7A359261CDCD734E0DCAA037E8FDDFE955CD9884B2533B38F8C09DAD32195E2AF178C42CB2E8B1130EC9378ECE49FCE579F048297ED9668AA6416DA94EE5D1A555778EBF12E1EF32D9D14DCE1909B52129F2F748DD06432C6B885C2959C384671F918DAA7AB99CBA2DD8EF9F7547742B6967ED251A26F353DD0CF8097A15498A3030D415ECC901D95F7B1647E8FE054380004B1735D9D31F3704DC914A76E2B8F0499FBDA8FBF01983ADF0FCD6EB918117B9D9410AB8F9CD52B08E209BA70F05E4A2C4707A98D57DDB5141E04C00698FA430F9E1269118212EF1771A7B1C2E3CC14FF298F7385B1E01C2A400573AB3B353E83F0E3FD7F94D8723406C067A4681E167637BD90"
boolmindmax = False
mindmaxfilepath = "C:/ServerFinder/GeoLite2-Country.mmdb"
mindmaxpath = "C:/ServerFinder/"
mindmaxfetchlink = "https://drive.usercontent.google.com/download?id=1hyZmPjGCzDixKY6HYzFPhoxodl29Elkm&export=download&authuser=0"
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
            print(f"GeoLite2 setup failed because of: {e}")
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

                    if server_data_dict and isinstance(server_data_dict,
                                                       dict) and 'gameid' in server_data_dict and 'location_data' in server_data_dict:
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


if __name__ == "__main__":
    place_id_input = int(input("Enter roblox game ID: "))

    if not mindmax_setup():
        print("GeoLite2 setup failed. Location lookups will not work for this run.")
    def main():
        gameid = fetch_serverid(place_id_input)

        final_servers = sorting_threading(place_id_input, gameid, cookietemp)

        print("\n--- Servers (Hong Kong & Singapore Only) ---")
        found_filtered_servers = False
        if final_servers:
            for server in final_servers:
                id = server.get('gameid', 'N/A')
                location_info = server.get('location_data', {})
                country_code = location_info.get('country_code', 'N/A')

                if country_code in ["HK", "SG"]:
                    base_share_url = "https://oqarshi.github.io/Invite/"
                    share_link = f"{base_share_url}?placeid={place_id_input}&serverid={id}"
                    print(f"Server in HK/SG Country Code: {country_code}, Link: {share_link}")
                    found_filtered_servers = True

        if not found_filtered_servers:
            print("No servers found in Hong Kong or Singapore.")
            print("Searching again in 10 seconds...")
            time.sleep(10)
            main()
    main()
    input("\nPress Enter to exit...")