import customtkinter as tk
import time
import os
import threading
import pygame as pg
from Roblox_Search_Script import main
cookie = None
path = "C:/ServerFinder/"
running = False
sound = None

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
        output(main(cookie, PlaceID))
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
            output("Searching for game Servers in HK and SG")
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
    sound_in = tk.CTkInputDialog(text="Input Name of Sound File:", title="Sound File")
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


if __name__ == "__main__":

    root = tk.CTk()
    root.geometry('800x550')
    root.title('funky functions')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    pg.mixer.init()

    main_frame = tk.CTkFrame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True, anchor="w")

    #Main
    left_frame = tk.CTkFrame(main_frame,width=350,height=500)
    left_frame.grid(row=0, column=0,pady=30)

    title_label =  tk.CTkLabel(left_frame,text='Roblox Server Search',font=tk.CTkFont(size=30,weight='bold'))
    title_label.pack(padx=50,pady=10,anchor="nw")

    label1 =  tk.CTkLabel(left_frame,text='Roblox Game ID',font=tk.CTkFont(size=20))
    label1.pack(padx=10,pady=(20, 10))

    PlaceID_textbox = tk.CTkTextbox(left_frame,height=25,width=400,font=tk.CTkFont(size=15),activate_scrollbars=False)
    PlaceID_textbox.pack(padx=10,pady=(5,10))

    label2 =  tk.CTkLabel(left_frame,text='Output',font=tk.CTkFont(size=20))
    label2.pack(padx=10,pady=(10, 10))

    Out_textbox = tk.CTkTextbox(left_frame,height=200,width=400,font=tk.CTkFont(size=15),state="disabled")
    Out_textbox.pack(padx=10,pady=(5,10))

    run_button = tk.CTkButton(left_frame,text='Run',command=Gui_main)
    run_button.pack(pady=5)

    #MISC
    Misc_frame = tk.CTkFrame(main_frame, width=250, height=150)
    Misc_frame.grid(row=0, column=1, padx=10, pady=30, sticky="ne")
    Misc_frame.grid_columnconfigure(0, weight=1)
    Misc_frame.grid_columnconfigure(1, weight=1)
    Misc_frame.grid_rowconfigure(0, weight=0)
    Misc_frame.grid_rowconfigure(1, weight=0)
    Misc_frame.grid_rowconfigure(2, weight=0)
    Misc_frame.grid_rowconfigure(3, weight=0)
    Misc_frame.grid_rowconfigure(4, weight=1)

    Misc_label = tk.CTkLabel(Misc_frame, text='Misc', font=tk.CTkFont(size=20, weight='bold'))
    Misc_label.grid(row=2, column=0, padx=10, pady=(5,10), sticky="ew")

    sound_button = tk.CTkButton(Misc_frame, text="Change Sound", command=choose_sound,
                                height=25, width=120, corner_radius=8)
    sound_button.grid(row=1, column=1, padx=(50,100), pady=(5,5), sticky="e")
    #cookie actions
    cookie_load_button = tk.CTkButton(Misc_frame, text="Load Cookies", command=load_cookie,
                                      height=25, width=120, corner_radius=8)
    cookie_load_button.grid(row=2, column=1, padx=(50,100), pady=(5,5), sticky="e")

    cookie_button = tk.CTkButton(Misc_frame, text="Save Cookies", command=save_cookie,
                                 height=25, width=120, corner_radius=8)
    cookie_button.grid(row=3, column=1, padx=(50,100), pady=(5,5), sticky="e")





    output("Innitializing...")
    root.mainloop()