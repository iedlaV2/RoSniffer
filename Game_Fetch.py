import requests
import uuid


def game_explore(reqfilter):
    games_dict = {}
    sessionID = str(uuid.uuid4())
    try:
        url = f"https://apis.roblox.com/explore-api/v1/get-sort-content?discoverPageSessionInfo={sessionID}&gameSetTargetId=671&gameSetTypeId=23&page=gamesPage&position=3&treatmentType=Carousel&cpuCores=12&maxResolution=1193x853&maxMemory=8192&networkType=4g&sessionId={sessionID}&sortId={reqfilter}"
        response = requests.get(url)
        response.raise_for_status()
        game_unparsed = response.json()
        games_lst = game_unparsed.get("games",[])
    except requests.exceptions.RequestException as e:
        return(e)
    print(games_lst)
    if games_lst:
        for game in games_lst:
            game_name = game.get("name")
            games_dict[game_name] = {
                'Player Count': game.get("playerCount"),
                'Game ID': game.get("rootPlaceId")
            }
        return games_dict
    else:
        return("Games not found")
#print(game_explore("top-playing-now"))

def roblox_search(search_content):
    search_return_dict = {}
    sessionID = str(uuid.uuid4())
    url = f"https://apis.roblox.com/search-api/omni-search?searchQuery={search_content}&pageToken=&sessionId={sessionID}&pageType=all"
    response = requests.get(url)
    response.raise_for_status()
    search_unparsed = response.json()
    search_return = search_unparsed.get("searchResults",[])
    if search_return:
        for ret in search_return:
            games = ret.get("contents",[])
            for game in games:
                game_name = game.get("name")
                game_PlaceID = game.get("rootPlaceId")
                search_return_dict[game_name] = game_PlaceID
        return search_return_dict
#print(roblox_search(""))

