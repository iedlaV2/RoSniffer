import customtkinter as tk
import time
import os
import threading
import pygame as pg
from Roblox_Search_Script import main,down_icon
cookie = None
path = "C:/ServerFinder/"
running = False
sound = None
country_filter = []
country_switch_vars = {}
def icon():
    try:
        if os.path.exists("C:/ServerFinder/logo.ico"):
            print("logo exists")
            pass
        else:
            os.chdir("C:/ServerFinder/")
            down_icon()
            print("downloaded logo")
    except Exception as e:
        return "Failed to load logo"
icon()
def output(text):
    timestamp = time.strftime("%H:%M:%S")
    Out_textbox.configure(state="normal")
    Out_textbox.insert("end", f"{timestamp}: {text}\n")
    Out_textbox.configure(state="disabled")
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
        if not running:
            running = True
            output(f"Searching for game Servers in {country_filter}")
            start_search_thread()
            running = False

        else:
            output(f"Already running for {PlaceID}")
    except Exception as e:
        print(e)
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

    except Exception as e:
        output(f"Failed to create directory '{path}'")
        return
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
def grids(frame):
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=0)
    frame.grid_rowconfigure(3, weight=0)
    frame.grid_rowconfigure(4, weight=0)
    frame.grid_rowconfigure(5, weight=1)
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

if __name__ == "__main__":
    root = tk.CTk()
    root.geometry('800x550')
    root.title('RoSniffer by Iedla')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    pg.mixer.init()
    root.iconbitmap("C:/ServerFinder/logo.ico")

    main_frame = tk.CTkFrame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True, anchor="w")
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)
    main_frame.grid_rowconfigure(0, weight=1)

    #Main
    left_frame = tk.CTkFrame(main_frame,width=350,height=500)
    left_frame.grid(row=0, column=0,pady=30,sticky="w")

    title_label =  tk.CTkLabel(left_frame,text='RoSniffer',font=tk.CTkFont(size=30,weight='bold'))
    title_label.pack(padx=50,pady=(8,0),anchor="n")

    description =  tk.CTkLabel(left_frame,text='A roblox server searcher',font=tk.CTkFont(size=10))
    description.pack(padx=10,pady=(0, 3))

    label1 =  tk.CTkLabel(left_frame,text='Roblox Game ID',font=tk.CTkFont(size=20))
    label1.pack(padx=10,pady=(8, 10))

    PlaceID_textbox = tk.CTkTextbox(left_frame,height=25,width=400,font=tk.CTkFont(size=15),activate_scrollbars=False)
    PlaceID_textbox.pack(padx=10,pady=(5,8))

    label2 =  tk.CTkLabel(left_frame,text='Output',font=tk.CTkFont(size=20))
    label2.pack(padx=10,pady=(5, 8))

    Out_textbox = tk.CTkTextbox(left_frame,height=200,width=400,font=tk.CTkFont(size=15),state="disabled")
    Out_textbox.pack(padx=10,pady=(5,10))

    run_button = tk.CTkButton(left_frame,text='Run',command=Gui_main)
    run_button.pack(pady=5)

    right_frame = tk.CTkFrame(main_frame)
    right_frame.grid(row=0, column=1, pady=30, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=0)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    #MISC
    Misc_frame = tk.CTkFrame(right_frame, width=250, height=150)
    Misc_frame.grid(row=0, column=1, padx=10, pady=30, sticky="ne")
    grids(Misc_frame)

    Misc_label = tk.CTkLabel(Misc_frame, text='Misc', font=tk.CTkFont(size=20, weight='bold'))
    Misc_label.grid(row=2, column=0, padx=10, pady=(5,10), sticky="ew")

    sound_button = tk.CTkButton(Misc_frame, text="Change Sound", command=choose_sound,
                                height=25, width=120, corner_radius=8)
    sound_button.grid(row=1, column=1, padx=(100,50), pady=(5,5), sticky="e")
    #cookie actions
    cookie_load_button = tk.CTkButton(Misc_frame, text="Load Cookies", command=load_cookie,
                                      height=25, width=120, corner_radius=8)
    cookie_load_button.grid(row=2, column=1, padx=(100,50), pady=(5,5), sticky="e")

    cookie_button = tk.CTkButton(Misc_frame, text="Save Cookies", command=save_cookie,
                                 height=25, width=120, corner_radius=8)
    cookie_button.grid(row=3, column=1, padx=(100,50), pady=(5,5), sticky="e")

    # Server Selector
    Server_frame = tk.CTkFrame(right_frame)
    Server_frame.grid(row=1, column=1, padx=10, pady=(0,10), sticky="nsew")
    Server_frame.grid_columnconfigure(0, weight=1)
    Server_label = tk.CTkLabel(Server_frame, text='Server Selection', font=tk.CTkFont(size=20, weight='bold'))
    Server_label.grid(row=0, column=0, padx=0, pady=(5, 5), sticky="ew")

    hk_bool = tk.StringVar(value="hk_off")
    hk_switch = tk.CTkSwitch(Server_frame, text="Hong Kong", command=lambda: switch_event("HK"),variable=hk_bool, onvalue="hk_on", offvalue="hk_off")
    hk_switch.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")
    sg_bool = tk.StringVar(value="sg_off")
    sg_switch = tk.CTkSwitch(Server_frame, text="Singapore", command=lambda:switch_event("SG"),variable=hk_bool, onvalue="sg_on", offvalue="sg_off")
    sg_switch.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")



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
                             variable=country_switch_vars["HK"], onvalue="hk on", offvalue="hk off")
    hk_switch.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
    sg_switch = tk.CTkSwitch(Server_frame, text="Singapore", command=lambda: switch_event("SG"),
                             variable=country_switch_vars["SG"], onvalue="sg on", offvalue="sg off")
    sg_switch.grid(row=1 + 1, column=0, padx=20, pady=(10, 5), sticky="ew")
    gb_switch = tk.CTkSwitch(Server_frame, text="United Kingdom", command=lambda: switch_event("GB"),
                             variable=country_switch_vars["GB"], onvalue="gb on", offvalue="gb off")
    gb_switch.grid(row=1 + 2, column=0, padx=20, pady=(10, 5), sticky="ew")
    fr_switch = tk.CTkSwitch(Server_frame, text="France", command=lambda: switch_event("FR"),
                             variable=country_switch_vars["FR"], onvalue="fr on", offvalue="fr off")
    fr_switch.grid(row=1 + 3, column=0, padx=20, pady=(10, 5), sticky="ew")
    de_switch = tk.CTkSwitch(Server_frame, text="Germany", command=lambda: switch_event("DE"),
                             variable=country_switch_vars["DE"], onvalue="de on", offvalue="de off")
    de_switch.grid(row=1 + 4, column=0, padx=20, pady=(10, 5), sticky="ew")
    jp_switch = tk.CTkSwitch(Server_frame, text="Japan", command=lambda: switch_event("JP"),
                             variable=country_switch_vars["JP"], onvalue="jp on", offvalue="jp off")
    jp_switch.grid(row=1, column=1, padx=20, pady=(10, 5), sticky="ew")
    in_switch = tk.CTkSwitch(Server_frame, text="India", command=lambda: switch_event("IN"),
                             variable=country_switch_vars["IN"], onvalue="in on", offvalue="in off")
    in_switch.grid(row=2, column=1, padx=20, pady=(10, 5), sticky="ew")
    au_switch = tk.CTkSwitch(Server_frame, text="Australia", command=lambda: switch_event("AU"),
                             variable=country_switch_vars["AU"], onvalue="au on", offvalue="au off")
    au_switch.grid(row=3, column=1, padx=20, pady=(10, 5), sticky="ew")
    kr_switch = tk.CTkSwitch(Server_frame, text="South Korea", command=lambda: switch_event("KR"),
                             variable=country_switch_vars["KR"], onvalue="kr on", offvalue="kr off")
    kr_switch.grid(row=4, column=1, padx=20, pady=(10, 5), sticky="ew")
    nl_switch = tk.CTkSwitch(Server_frame, text="Netherlands", command=lambda: switch_event("NL"),
                             variable=country_switch_vars["NL"], onvalue="nl on", offvalue="nl off")
    nl_switch.grid(row=5, column=1, padx=20, pady=(10, 5), sticky="ew")


    output("Innitializing...")
    root.mainloop()