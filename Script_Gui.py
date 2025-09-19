import customtkinter as tk
import time
import os
import threading
from Roblox_Search_Script import main
cookie = None
path = "C:/ServerFinder/"
running = False

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
            PlaceID_textbox.configure(state="disabled")
            running = True
            output("Searching for game Servers in HK and SG")
            start_search_thread()
            running = False
            PlaceID_textbox.configure(state="enabled")
        else:
            output(f"Already running for {PlaceID}")
    except Exception as e:
        print(e)



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




root = tk.CTk()
root.geometry('500x600')
root.title('funky functions')

title_label =  tk.CTkLabel(root,text='Roblox Server Search',font=tk.CTkFont(size=30,weight='bold'))
title_label.pack(padx=10,pady=(30,10))

label1 =  tk.CTkLabel(root,text='Roblox Game ID',font=tk.CTkFont(size=20))
label1.pack(padx=10,pady=(20, 10))

PlaceID_textbox = tk.CTkTextbox(root,height=25,width=400,font=tk.CTkFont(size=15),activate_scrollbars=False)
PlaceID_textbox.pack(padx=10,pady=(10,10))

label2 =  tk.CTkLabel(root,text='Output',font=tk.CTkFont(size=20))
label2.pack(padx=10,pady=(10, 10))

Out_textbox = tk.CTkTextbox(root,height=200,width=400,font=tk.CTkFont(size=15),state="disabled")
Out_textbox.pack(padx=10,pady=(10,10))

run_button = tk.CTkButton(root,text='Run',command=Gui_main)
run_button.pack()

cookie_button = tk.CTkButton(root, text="Save Cookies", command=save_cookie,height=5,width=15,corner_radius=3)
cookie_button.pack(padx=10, pady=5, side=tk.BOTTOM, anchor=tk.SE)

cookie_load_button = tk.CTkButton(root, text="Load Cookies", command=load_cookie,height=5,width=15,corner_radius=3)
cookie_load_button.pack(padx=10, pady=5, side=tk.BOTTOM, anchor=tk.SE)




output("Innitializing...")
root.mainloop()