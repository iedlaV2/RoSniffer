import customtkinter as tk
import time, os, threading,queue,pyperclip,webbrowser
import pygame as pg
import matplotlib.font_manager as fm
from PIL import Image
from Roblox_Search_Script import main,down_icon,down_sound
from Game_Fetch import game_explore, roblox_search
cookie = None
path = "C:/ServerFinder/"
sound = None
selection = "Top Playing"
custom_font = "Calibri"
country_filter = []
country_switch_vars = {}
sort_selection_dict = {
    "Top Trending":"top-trending",
    "Top Playing":"top-playing-now",
    "Up And Coming":"up-and-coming",
    "Fun with Friends":"fun-with-friends"
}
all_fetched_games = {}
cur_page_index = 0
items_per_page = 20
total_pages = 0
page_info_label = None
prev_page_button = None
next_page_button = None
fetch_in_progress = False


#Icon, Sounds & Misc
def icon_and_sound():
    global sound
    try:
        if os.path.exists("C:/ServerFinder/logo.ico"):
            pass
        else:
            os.chdir("C:/ServerFinder/")
            down_icon()
            sound = "ding.mp3"
        if os.path.exists("C:/ServerFinder/ding.mp3"):
            pass
        else:
            os.chdir("C:/ServerFinder/")
            down_sound()
    except Exception as e:
        return "Failed to load logo"
icon_and_sound()
def load_sound():
    global sound
    try:
        with open("C:/ServerFinder/sound_cfg.txt", "r") as f:
            sound = f.read()
            f.close()
    except Exception as e:
        sound = "ding.mp3"
load_sound()
def play_sound(sound_effect):
    try:
        sound = pg.mixer.Sound(sound_effect)
        sound.play()
    except Exception as e:
        print(f"Error playing sound {sound_effect}: {e}")
def choose_sound():
    global sound
    sound_in = tk.CTkInputDialog(text="Input Name of Sound File:", title="Sound File",)
    extract = sound_in.get_input()
    sound = extract.strip()
    if not sound:
        output("Sound file not entered.")
        return
    try:
        os.makedirs(path, exist_ok=True)
        if os.path.exists(path):
            output(f"Directory exists")
            if os.path.exists(sound):
                output(f"Found sound file: '{sound}'")
                full_path = os.path.join(path, "sound_cfg.txt")
                try:
                    with open(full_path, "w") as f:
                        f.write(sound)
                except Exception as e:
                    output(f"Failed to save sound to '{full_path}': {e}")
            else:
                output(f"Failed to find sound file: '{sound}'")

    except Exception as e:
        output(f"Failed to create directory '{path}'")
        return
def output(text):
    timestamp = time.strftime("%H:%M:%S")
    Out_textbox.configure(state="normal")
    Out_textbox.insert("end", f"{timestamp}: {text}\n")
    Out_textbox.configure(state="disabled")
def grids(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=0)
    frame.grid_rowconfigure(3, weight=0)
    frame.grid_rowconfigure(4, weight=0)
    frame.grid_rowconfigure(5, weight=1)
def clipboard(copy):
    pyperclip.copy(copy)
def send_website(gameid):
    url = f"https://www.roblox.com/games/{gameid}"
    webbrowser.open(url)



#Cookies
def save_cookie():
    global cookie
    Cookie_in = tk.CTkInputDialog(text="Input Roblox Cookie:", title="Cookie")
    extract = Cookie_in.get_input()
    cookie = extract.strip()
    if not cookie:
        output("Cookie not entered.")
        return
    try:
        os.makedirs(path, exist_ok=True)
        output(f"Directory exists")
    except Exception as e:
        output(f"Failed to create directory '{path}'")
        return

    full_path = os.path.join(path, "cookie.txt")

    try:
        with open(full_path, "w") as f:
            f.write(cookie)
        output(f"Saved Cookie to: {full_path}")
    except Exception as e:
        output(f"Failed to save cookie to '{full_path}': {e}")
def load_cookie():
    output("Loading Cookie...")
    global cookie
    try:
        os.chdir("C:/ServerFinder/")
        with open("cookie.txt", "r") as f:
            cookie = f.read()
            f.close()
        output(f"Loaded Cookie")
    except Exception as e:
        output(f"Failed to load cookie because of '{e}'")
# Server Search
def run_search_script():
    try:
        output(main(cookie, PlaceID,country_filter))
        play_sound(sound)
    except Exception as e:
        output(f"Failed to run search script because of {e}")
def start_search_thread():
    search_thread = threading.Thread(target=run_search_script)
    search_thread.daemon = True
    search_thread.start()
def Gui_main():
    global running
    global PlaceID
    extract = PlaceID_textbox.get("0.0", "end")
    PlaceID = extract.strip()
    if not cookie or not PlaceID:
        output("No Cookie or GameID")
        return
    try:
        output(f"Searching for game Servers in {country_filter}")
        start_search_thread()
    except Exception as e:
        print(e)
def switch_event(country):
    global country_filter
    on_substring = "on"
    off_substring = "off"
    switch_var = country_switch_vars[country]
    check_switch = switch_var.get()
    if on_substring in check_switch:
        country_filter.append(country)
    if off_substring in check_switch:
        country_filter.remove(country)

#Discovery
fetch_in_progress = False
game_fetch = queue.Queue()
def sort_selection():
    global explore_filter, fetch_in_progress, cur_page_index, all_fetched_games, total_pages

    if fetch_in_progress:
        output("Fetch already in progress. Please wait.")
        return

    explore_filter = sort_selection_dict[selection]
    output(f"--- Fetching games for: {explore_filter} ---")
    fetch_in_progress = True

    for widget in out_frame.winfo_children():
        widget.destroy()
    tk.CTkLabel(out_frame, text="Loading games...", font=(custom_font, 12)).pack(pady=10)


    if prev_page_button: prev_page_button.configure(state="disabled")
    if next_page_button: next_page_button.configure(state="disabled")
    if page_info_label: page_info_label.configure(text="Loading...")

    start_disc_fetch(explore_filter)
    root.after(100, check_game_fetch_queue)
def display_on_frame(gamelst):
    for widget in out_frame.winfo_children():
        widget.destroy()

    if not isinstance(gamelst, dict) or not gamelst:
        tk.CTkLabel(out_frame, text="No games found or error fetching games.", font=tk.CTkFont(family=custom_font, size=12)).pack(pady=10)
        return

    for game_name, game_id in gamelst.items():
        player_count = game_id.get('Player Count', 'N/A')
        game_id = game_id.get('Game ID', 'N/A')
        game_frame = tk.CTkFrame(out_frame, corner_radius=10, border_color="#141414")
        game_frame.pack(fill="x", pady=5, padx=10)

        game_name_label = tk.CTkLabel(game_frame, text=game_name, font=tk.CTkFont(family=custom_font, size=25, weight="bold"))
        game_name_label.pack(anchor="w")

        player_count_label = tk.CTkLabel(game_frame, text=f"Players: {player_count}", font=tk.CTkFont(family=custom_font, size=15))
        player_count_label.pack(anchor="w")

        game_id_label = tk.CTkLabel(game_frame, text=f"Game ID: {game_id}", font=tk.CTkFont(family=custom_font, size=15))
        game_id_label.pack(anchor="w")

        gameid_copy_button = tk.CTkButton(game_frame,text="Copy Game ID",fg_color="transparent",hover_color="royal blue",border_color="#222222",font=tk.CTkFont(family=custom_font, size=15),command=lambda current_game_id=game_id: clipboard(current_game_id))
        gameid_copy_button.pack(anchor="e")

        gameid_send_button = tk.CTkButton(game_frame,text="Go to Website",fg_color="transparent",hover_color="royal blue",border_color="#222222",font=tk.CTkFont(family=custom_font, size=15),command=lambda current_game_id=game_id: send_website(current_game_id))
        gameid_send_button.pack(anchor="e")
def check_game_fetch_queue():
    global all_fetched_games, fetch_in_progress, cur_page_index, total_pages

    if not fetch_in_progress:
        return

    try:
        fetched_data = game_fetch.get(block=False)

        if isinstance(fetched_data, Exception):
            all_fetched_games = {}
            for widget in out_frame.winfo_children(): widget.destroy()
            tk.CTkLabel(out_frame, text=f"Error: {fetched_data}", font=(custom_font, 12), text_color="red").pack(
                pady=10)
        else:
            output("Games fetched successfully!")
            all_fetched_games = fetched_data
            cur_page_index = 0
            total_games = len(all_fetched_games)
            total_pages = (total_games + items_per_page - 1) // items_per_page
            display_current_page()

        fetch_in_progress = False

    except queue.Empty:
        root.after(100, check_game_fetch_queue)

    except Exception as e:
        output(f"An unexpected error occurred while getting games from queue: {e}")
        all_fetched_games = {}
        fetch_in_progress = False
def store_selection(choice):
    global selection
    selection = choice
def run_disc_fetch(reqfilter):
    try:
        result = game_explore(reqfilter)
        game_fetch.put(result)
    except Exception as e:
        game_fetch.put(e)
def start_disc_fetch(reqfilter):
    disc_thread = threading.Thread(target=run_disc_fetch,args=(reqfilter,))
    disc_thread.daemon = True
    disc_thread.start()
def display_current_page():
    global cur_page_index, items_per_page, all_fetched_games, total_pages

    for widget in out_frame.winfo_children():
        widget.destroy()

    if not all_fetched_games:
        tk.CTkLabel(out_frame, text="No games to display.", font=tk.CTkFont(family=custom_font, size=12)).pack(pady=10)
        if prev_page_button: prev_page_button.configure(state="disabled")
        if next_page_button: next_page_button.configure(state="disabled")
        if page_info_label: page_info_label.configure(text="Page 0/0")
        return

    game_names = list(all_fetched_games.keys())
    start_index = cur_page_index * items_per_page
    end_index = min(start_index + items_per_page, len(game_names))

    if start_index >= len(game_names):
        tk.CTkLabel(out_frame, text="No more games on this page.", font=tk.CTkFont(family=custom_font, size=12)).pack(pady=10)
        return

    for i in range(start_index, end_index):
        game_name = game_names[i]
        game_details_dict = all_fetched_games[game_name]

        player_count = game_details_dict.get('Player Count', 'N/A')
        game_id = game_details_dict.get('Game ID', 'N/A')

        game_frame = tk.CTkFrame(out_frame, corner_radius=10, border_color="#141414")
        game_frame.pack(fill="x", pady=5, padx=10, ipady=5)

        game_name_label = tk.CTkLabel(game_frame, text=game_name, font=tk.CTkFont(family=custom_font, size=20, weight="bold"))
        game_name_label.pack(anchor="w", padx=5)

        player_count_label = tk.CTkLabel(game_frame, text=f"Players: {player_count}", font=tk.CTkFont(family=custom_font, size=12))
        player_count_label.pack(anchor="w", padx=5)

        game_id_label = tk.CTkLabel(game_frame, text=f"Game ID: {game_id}", font=tk.CTkFont(family=custom_font, size=12))
        game_id_label.pack(anchor="w", padx=5)


        button_sub_frame = tk.CTkFrame(game_frame, fg_color="transparent")
        button_sub_frame.pack(fill="x", anchor="e", pady=(5,0))
        button_sub_frame.grid_columnconfigure(0, weight=1)
        button_sub_frame.grid_columnconfigure(1, weight=0)
        button_sub_frame.grid_columnconfigure(2, weight=0)

        gameid_copy_button = tk.CTkButton(button_sub_frame,text="Copy ID",fg_color="transparent",hover_color="royal blue",border_color="#222222",font=tk.CTkFont(family=custom_font, size=12),command=lambda current_game_id=game_id: clipboard(current_game_id))
        gameid_copy_button.grid(row=0, column=1, padx=(0,5), pady=2, sticky="e")

        gameid_send_button = tk.CTkButton(button_sub_frame,text="Go to Website",fg_color="transparent",hover_color="royal blue",border_color="#222222",font=tk.CTkFont(family=custom_font, size=12),command=lambda current_game_id=game_id: send_website(current_game_id))
        gameid_send_button.grid(row=0, column=2, padx=(0,5), pady=2, sticky="e")
    update_navigation_buttons()
def update_navigation_buttons():
    global cur_page_index, total_pages

    if page_info_label:
        page_info_label.configure(text=f"Page {cur_page_index + 1}/{total_pages}")

    if prev_page_button:
        if cur_page_index > 0:
            prev_page_button.configure(state="normal")
        else:
            prev_page_button.configure(state="disabled")

    if next_page_button:
        if cur_page_index < total_pages - 1:
            next_page_button.configure(state="normal")
        else:
            next_page_button.configure(state="disabled")
def go_to_previous_page():
    global cur_page_index
    if cur_page_index > 0:
        cur_page_index -= 1
        display_current_page()
def go_to_next_page():
    global cur_page_index, total_pages
    if cur_page_index < total_pages - 1:
        cur_page_index += 1
        display_current_page()

def server_search_page(parent_frame):
    global Out_textbox, PlaceID_textbox, content_frame
    content_frame = tk.CTkFrame(parent_frame,corner_radius=0,fg_color="transparent")
    content_frame.grid(row=0, column=1, sticky="nsew")
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=0)
    content_frame.grid_rowconfigure(0, weight=1)

    left_frame = tk.CTkFrame(content_frame,width=350,height=500)
    left_frame.grid(row=0, column=0,pady=30,sticky="w")

    title_label =  tk.CTkLabel(left_frame,text='Roblox Server Search',font=tk.CTkFont(family=custom_font,size=25,weight='bold'))
    title_label.pack(pady=(10,10),anchor="n")

    label1 =  tk.CTkLabel(left_frame,text='Roblox Game ID',font=tk.CTkFont(family=custom_font,size=20))
    label1.pack(padx=10,pady=(8, 10))

    PlaceID_textbox = tk.CTkTextbox(left_frame,height=25,width=400,font=tk.CTkFont(family=custom_font,size=15),activate_scrollbars=False)
    PlaceID_textbox.pack(padx=10,pady=(5,8))

    label2 =  tk.CTkLabel(left_frame,text='Output',font=tk.CTkFont(family=custom_font,size=20))
    label2.pack(padx=10,pady=(5, 8))

    Out_textbox = tk.CTkTextbox(left_frame,height=200,width=400,font=tk.CTkFont(family=custom_font,size=15),state="disabled")
    Out_textbox.pack(padx=10,pady=(5,10))

    run_button = tk.CTkButton(left_frame,text='Run',command=Gui_main,fg_color='royal blue',font=tk.CTkFont(family=custom_font))
    run_button.pack(pady=5)

    right_frame = tk.CTkFrame(content_frame)
    right_frame.grid(row=0, column=1, pady=30, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=0)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    #MISC
    Misc_frame = tk.CTkFrame(right_frame, width=250, height=150)
    Misc_frame.grid(row=0, column=1, padx=10, pady=30, sticky="ne")
    grids(Misc_frame)

    Misc_label = tk.CTkLabel(Misc_frame, text='Misc', font=tk.CTkFont(family=custom_font,size=20, weight='bold'))
    Misc_label.grid(row=2, column=0, padx=(20,0), pady=(5,10), sticky="ew")

    sound_button = tk.CTkButton(Misc_frame, text="Change Sound", command=choose_sound,
                                height=25, width=120, corner_radius=8,fg_color='royal blue',font=tk.CTkFont(family=custom_font))
    sound_button.grid(row=1, column=1, padx=(100,50), pady=(5,5), sticky="e")
    #cookie actions
    cookie_load_button = tk.CTkButton(Misc_frame, text="Load Cookies", command=load_cookie,
                                      height=25, width=120, corner_radius=8,fg_color='royal blue',font=tk.CTkFont(family=custom_font))
    cookie_load_button.grid(row=2, column=1, padx=(100,50), pady=(5,5), sticky="e")

    cookie_button = tk.CTkButton(Misc_frame, text="Save Cookies", command=save_cookie,
                                 height=25, width=120, corner_radius=8,fg_color='royal blue',font=tk.CTkFont(family=custom_font))
    cookie_button.grid(row=3, column=1, padx=(100,50), pady=(5,5), sticky="e")

    # Server Selector
    Server_frame = tk.CTkFrame(right_frame)
    Server_frame.grid(row=1, column=1, padx=10, pady=(0,10), sticky="nsew")
    Server_frame.grid_columnconfigure(0, weight=1)
    Server_label = tk.CTkLabel(Server_frame, text='Server Selection', font=tk.CTkFont(family=custom_font,size=20, weight='bold'))
    Server_label.grid(row=0, column=0, padx=0, pady=(5, 5), sticky="ew")

    country_switch_vars["HK"] = tk.StringVar(value="hk off")
    country_switch_vars["SG"] = tk.StringVar(value="sg off")
    country_switch_vars["GB"] = tk.StringVar(value="gb off")
    country_switch_vars["FR"] = tk.StringVar(value="fr off")
    country_switch_vars["DE"] = tk.StringVar(value="de off")
    country_switch_vars["JP"] = tk.StringVar(value="jp off")
    country_switch_vars["IN"] = tk.StringVar(value="in off")
    country_switch_vars["AU"] = tk.StringVar(value="au off")
    country_switch_vars["KR"] = tk.StringVar(value="kr off")
    country_switch_vars["NL"] = tk.StringVar(value="nl off")

    hk_switch = tk.CTkSwitch(Server_frame, text="Hong Kong", command=lambda: switch_event("HK"),
                             variable=country_switch_vars["HK"], onvalue="hk on", offvalue="hk off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    hk_switch.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
    sg_switch = tk.CTkSwitch(Server_frame, text="Singapore", command=lambda: switch_event("SG"),
                             variable=country_switch_vars["SG"], onvalue="sg on", offvalue="sg off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    sg_switch.grid(row=1 + 1, column=0, padx=20, pady=(10, 5), sticky="ew")
    gb_switch = tk.CTkSwitch(Server_frame, text="United Kingdom", command=lambda: switch_event("GB"),
                             variable=country_switch_vars["GB"], onvalue="gb on", offvalue="gb off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    gb_switch.grid(row=1 + 2, column=0, padx=20, pady=(10, 5), sticky="ew")
    fr_switch = tk.CTkSwitch(Server_frame, text="France", command=lambda: switch_event("FR"),
                             variable=country_switch_vars["FR"], onvalue="fr on", offvalue="fr off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    fr_switch.grid(row=1 + 3, column=0, padx=20, pady=(10, 5), sticky="ew")
    de_switch = tk.CTkSwitch(Server_frame, text="Germany", command=lambda: switch_event("DE"),
                             variable=country_switch_vars["DE"], onvalue="de on", offvalue="de off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    de_switch.grid(row=1 + 4, column=0, padx=20, pady=(10, 5), sticky="ew")
    jp_switch = tk.CTkSwitch(Server_frame, text="Japan", command=lambda: switch_event("JP"),
                             variable=country_switch_vars["JP"], onvalue="jp on", offvalue="jp off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    jp_switch.grid(row=1, column=1, padx=20, pady=(10, 5), sticky="ew")
    in_switch = tk.CTkSwitch(Server_frame, text="India", command=lambda: switch_event("IN"),
                             variable=country_switch_vars["IN"], onvalue="in on", offvalue="in off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    in_switch.grid(row=2, column=1, padx=20, pady=(10, 5), sticky="ew")
    au_switch = tk.CTkSwitch(Server_frame, text="Australia", command=lambda: switch_event("AU"),
                             variable=country_switch_vars["AU"], onvalue="au on", offvalue="au off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    au_switch.grid(row=3, column=1, padx=20, pady=(10, 5), sticky="ew")
    kr_switch = tk.CTkSwitch(Server_frame, text="South Korea", command=lambda: switch_event("KR"),
                             variable=country_switch_vars["KR"], onvalue="kr on", offvalue="kr off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    kr_switch.grid(row=4, column=1, padx=20, pady=(10, 5), sticky="ew")
    nl_switch = tk.CTkSwitch(Server_frame, text="Netherlands", command=lambda: switch_event("NL"),
                             variable=country_switch_vars["NL"], onvalue="nl on", offvalue="nl off",font=tk.CTkFont(family=custom_font),
                             fg_color='grey',progress_color='royal blue')
    nl_switch.grid(row=5, column=1, padx=20, pady=(10, 5), sticky="ew")
    output("Innitializing...")
    return content_frame
def discover_page(parent_frame):
    global discover_content_frame, out_frame, page_info_label, prev_page_button, next_page_button
    discover_content_frame = tk.CTkFrame(parent_frame, corner_radius=0,fg_color="transparent")
    discover_content_frame.grid(row=0, column=1, sticky="nsew")
    discover_content_frame.grid_columnconfigure(0, weight=4)
    discover_content_frame.grid_columnconfigure(1, weight=1)
    discover_content_frame.grid_rowconfigure(0, weight=1)
    discover_title_label =  tk.CTkLabel(discover_content_frame,text='Roblox Game Discovery',font=tk.CTkFont(family=custom_font,size=25,weight='bold'))
    discover_title_label.grid(row=0,column=0,pady=0,sticky="n")

    discover_left_frame = tk.CTkFrame(discover_content_frame)
    discover_left_frame.grid(row=0, column=0,pady=50,sticky="nsew")
    discover_left_frame.grid_columnconfigure(0, weight=1)
    discover_left_frame.grid_rowconfigure(0, weight=1)
    discover_left_frame.grid_rowconfigure(1, weight=0)

    out_frame = tk.CTkScrollableFrame(discover_left_frame,width=575,height=350)
    out_frame.grid(row=0, column=0,pady=0,padx=0,sticky="nsew")

    # Pagination Controls Frame (New)
    pagination_frame = tk.CTkFrame(discover_left_frame, fg_color="transparent")
    pagination_frame.grid(row=1, column=0, pady=(10,0), sticky="ew")
    pagination_frame.grid_columnconfigure(0, weight=1)
    pagination_frame.grid_columnconfigure(1, weight=1)
    pagination_frame.grid_columnconfigure(2, weight=1)

    prev_page_button = tk.CTkButton(pagination_frame, text="Previous", command=go_to_previous_page, state="disabled",
                                    fg_color="royal blue", text_color="white", font=tk.CTkFont(family=custom_font, size=12))
    prev_page_button.grid(row=0, column=0, padx=5, sticky="e")

    page_info_label = tk.CTkLabel(pagination_frame, text="Page 0/0", font=tk.CTkFont(family=custom_font, size=12))
    page_info_label.grid(row=0, column=1, padx=5)

    next_page_button = tk.CTkButton(pagination_frame, text="Next", command=go_to_next_page, state="disabled",
                                    fg_color="royal blue", text_color="white", font=tk.CTkFont(family=custom_font, size=12))
    next_page_button.grid(row=0, column=2, padx=5, sticky="w")


    discover_right_frame = tk.CTkFrame(discover_content_frame)
    discover_right_frame.grid(row=0, column=1, pady=0, sticky="nsew")
    discover_right_frame.grid_rowconfigure(0, weight=0)
    discover_right_frame.grid_rowconfigure(1, weight=0)
    discover_right_frame.grid_rowconfigure(2, weight=0)
    discover_right_frame.grid_rowconfigure(3, weight=0)
    discover_right_frame.grid_rowconfigure(4, weight=0)
    discover_right_frame.grid_rowconfigure(5, weight=0)
    discover_right_frame.grid_rowconfigure(6, weight=0)
    discover_right_frame.grid_columnconfigure(0, weight=1)

    discover_right_label = tk.CTkLabel(discover_right_frame,text="Filters",font=tk.CTkFont(family=custom_font,size=25,weight='bold'))
    discover_right_label.grid(row=0,column=0,pady=(45,10),padx=45,sticky="n")

    filter_label_sort = tk.CTkLabel(discover_right_frame, text="Sorting",
                                       font=tk.CTkFont(family=custom_font, size=15, weight='bold'))
    filter_label_sort.grid(row=1, column=0, pady=10, padx=0, sticky="w")

    sort_box = tk.CTkComboBox(discover_right_frame,values=["Top Playing","Top Trending","Up And Coming","Fun with Friends"],
                              command=store_selection,
                              state="readonly")
    sort_box.grid(row=2,column=0,pady=10,sticky="n")
    sort_box.set(selection)

    sort_button = tk.CTkButton(discover_right_frame, text="Fetch Games", compound="left", command=sort_selection,
                              anchor="center",
                              fg_color="royal blue", text_color="white",
                              font=tk.CTkFont(family=custom_font))
    sort_button.grid(row=3, column=0, pady=10, sticky="n", )

    return discover_content_frame



class App(tk.CTk):
    def __init__(self):
        super().__init__()
        global custom_font, main_frame
        self.geometry('1000x600')
        self.title('RoSniffer',)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        pg.mixer.init()
        pg.mixer.music.set_volume(0.5)
        self.iconbitmap("C:/ServerFinder/logo.ico")

        main_frame = tk.CTkFrame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True, anchor="w")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_rowconfigure(0, weight=1)

        #SideBar
        side_frame = tk.CTkFrame(main_frame)
        side_frame.grid(row=0, column=0, pady=10,padx=10,sticky="nsew")
        side_frame.grid_columnconfigure(0, weight=1)
        side_frame.grid_rowconfigure(0, weight=0)
        side_frame.grid_rowconfigure(1, weight=0)
        side_frame.grid_rowconfigure(2, weight=0)
        side_frame.grid_rowconfigure(3, weight=0)
        side_frame.grid_rowconfigure(4, weight=0)
        side_frame.grid_rowconfigure(5, weight=1)
        side_frame.grid_rowconfigure(6, weight=0)
        side_frame.grid_rowconfigure(7, weight=0)

        side_logo = tk.CTkImage(dark_image=Image.open("C:/ServerFinder/logo.ico"),size=(30,30))
        side_title =tk.CTkLabel(side_frame,text='RoSniffer',image=side_logo,compound="top",font=tk.CTkFont(family=custom_font,size=35,weight='bold'))
        side_title.grid(row=0,column=0,pady=(20,0),sticky="ew")
        side_description =  tk.CTkLabel(side_frame,text='A roblox server searcher',font=tk.CTkFont(family=custom_font,size=10))
        side_description.grid(row=1,column=0,pady=(0, 3))

        side_label =  tk.CTkLabel(side_frame,text='Features',font=tk.CTkFont(family=custom_font,size=20,weight="bold"))
        side_label.grid(row=2,column=0,padx=10,pady=(30, 1),sticky='w')
        button_btn = tk.CTkButton(side_frame,text="Server Search",compound="left",command=show_server_search_page,anchor="center",
                                  fg_color="transparent",text_color="white",hover_color='royal blue',font=tk.CTkFont(family=custom_font,size=15))
        button_btn.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="ew",)
        button_btn = tk.CTkButton(side_frame,text="Game Explorer",compound="left",command=show_discover_page,anchor="center",
                                  fg_color="transparent",text_color="white",hover_color='royal blue',font=tk.CTkFont(family=custom_font,size=15))
        button_btn.grid(row=4, column=0, padx=0, pady=(10, 5), sticky="ew",)
        credit_label = tk.CTkLabel(side_frame,text='Made by Iedla',font=tk.CTkFont(family=custom_font,size=12,weight="bold"))
        credit_label.grid(row=6, column=0, padx=10, pady=(10, 5), sticky="sw")
        credit_button = tk.CTkButton(side_frame,text='Github Repo',fg_color="royal blue",text_color="white",
                                     font=tk.CTkFont(family=custom_font,size=12),command=lambda: webbrowser.open("https://github.com/IedlaV2/RoSniffer"),)
        credit_button.grid(row=7, column=0, padx=10, pady=(0, 5), sticky="ew")

        main_content_area_frame = tk.CTkFrame(main_frame, corner_radius=0, fg_color="transparent")
        main_content_area_frame.grid(row=0, column=1, sticky="nsew")
        main_content_area_frame.grid_rowconfigure(0, weight=1)
        main_content_area_frame.grid_columnconfigure(0, weight=1)

        server_search_page_frame = server_search_page(main_content_area_frame)
        discover_page_frame = discover_page(main_content_area_frame)
        discover_content_frame.grid_forget()

        all_pages = [server_search_page_frame, discover_page_frame]

def show_server_search_page():
    discover_content_frame.grid_forget()
    server_search_page(main_frame)
def show_discover_page():
    content_frame.grid_forget()
    discover_page(main_frame)

if __name__ == '__main__':
    root = App()
    root.mainloop()