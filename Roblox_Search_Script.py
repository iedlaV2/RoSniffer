import requests
import concurrent.futures
import functools
import time
import os
import subprocess
import geoip2.database
import json

cookietemp = "CAEaAhAB.848AD73E11AFCD2C9291F71A7FC02CFF2607032FD4CD3ABFEB57A6EF51F1FFCC4A5BB9A9B93500B6FFF1796EC4327B6F8ABD92A907CEA8235EE25F34C878B92B7D485AC502E27D3DB982B288406D5C603DEF173A17DDFDA264772F3948D2A22D57E1F6DDA234C44A77B7707B54CDC2EB8FCFE4FA63276FF9DE8760A58D69CCB5A33B510F62EA069208A42742F9E4AB1250E3ED0F36DC27715E0C5E439DF39A99F10A404F01FD29F11F980B67395480599A796156E4719BB5B4929577D4D5166428F863B94E2FC25BF144591F570EE3F0745C6FA1809DB92344D956905E0EEADF0A70AB8909F71EDBE64B6D65B5A1A3E1F62B8AFD8949B9F18E4DDB55BF5F1C1A770067EAC4F6279EEC367BF1E9456BC0710002BC254397A23263D4756B8D77DC4DFBA43F4EFAC777178715DED1FAB6A56DBB82A73981980C5048213929DF85857C84AFECAFA05269D5C95D4BBCABD9B64BEE044BB901F41F3E0485E7E895949577AF521AEB741F2BE21F4B656BBFDE01334355F1B2EACDF8D3B919E83BDAB5FE77BBA94719A05791B386284D5064DB7BE7E015EE732A5487F991AC248F4172654D4B40DEC5811B77307FE7BEB185485E89601B14A4D95D2A5C48DEBFA4D5061391B6844CAAFDDD83F55AA4C1F7A82B5B2D1ACEEDD3A2CC99E3870DA0D93046C06AC48228991118E6B52EABC35FF31251B0207A6D88D420066C484C6193BB79624FF951F5C566E5E208A7AD1B4E812018E70F7897826B6C54CD3A60C19B61AA767B2D05696E6AE14F638818BC17441F2D0DF687C54E63F78A949427CB75CD1B0414C9727128A19C470A50015033150439648BCDD27BCA38EED0A9D5D7D32F7F1DB6FE6BC33A9C4F5F0C2713B3FA0FF959E59ACCC35349FA17E848FD37B385F3EF6455B604D3BCB3E6766D3A6EE32838A95799DDA5E6D8C2EAB22215199933A4403A0F8CB1FD35882E4B878213E394418EC8AA06FC139FC84103BE1EB0673A173ADEA6B361FE457C3C33441D0DC6DD8C9348D2B0A914096D99E33FA82DB854DF264AF8282C3A7A17701A56D0DA1A68DA4D76DC81C7CEDA8C4C73C37AB269176C3C90135A7DCCE0DB42A89297BC723D1C400177D66FE7C5E2942F6FA2E4DBA30E7EF4C55BB74F36D0617A028D6EF8E180CB8A0FB3592ADFDF0D68DD8CFB2D700D3B7DBFF36B6BC4F9341AC6F8F03D25843BCF3559E2"
boolmindmax = False
mindmaxfilepath = "C:/ServerFinder/GeoLite2-Country.mmdb"
mindmaxpath = "C:/ServerFinder/"
mindmaxfetchlink = "https://release-assets.githubusercontent.com/github-production-release-asset/249855791/376cbf60-48a9-49ea-ab12-dfbcfb247738?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-09-18T11%3A45%3A22Z&rscd=attachment%3B+filename%3DGeoLite2-Country.mmdb&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-09-18T10%3A44%3A34Z&ske=2025-09-18T11%3A45%3A22Z&sks=b&skv=2018-11-09&sig=iFv6LJ2X%2BqOtEdVuWDibgnh2ACOUpTq9%2FVpDJof386A%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHViaXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc1ODE5Mzk0OSwibmJmIjoxNzU4MTkzNjQ5LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.jpyJ-2Hr_Xgblt8KdQ0uuszitZzwxNNdLpRnPnk1z6I&response-content-disposition=attachment%3B%20filename%3DGeoLite2-Country.mmdb&response-content-type=application%2Foctet-stream"


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