import tkinter as tk
import os
import sys
import ctypes
import keyboard
import time

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

VIDEO_PATH = resource_path("rick.avi")


def block_system_keys():
    keyboard.block_key('left windows')
    keyboard.block_key('right windows')
    keyboard.add_hotkey('alt+tab', lambda: None, suppress=True)
    keyboard.add_hotkey('ctrl+esc', lambda: None, suppress=True)
    keyboard.add_hotkey('alt+f4', lambda: None, suppress=True)

def secret_exit():
    ctypes.windll.winmm.mciSendStringW("close rickvideo", None, 0, 0)
    os.system(f"taskkill /f /pid {os.getpid()}")

def activate_rickroll():
    smiley_label.destroy()
    text_label.destroy()
    support_label.destroy()
    secret_hint_label.destroy()
    
    root.configure(bg='black')
    root.config(cursor="no")

    hwnd = root.winfo_id()
    
    open_command = f'open "{VIDEO_PATH}" type mpegvideo alias rickvideo style child parent {hwnd}'
    ctypes.windll.winmm.mciSendStringW(open_command, None, 0, 0)
    
    root_w = root.winfo_screenwidth()
    root_h = root.winfo_screenheight()
    ctypes.windll.winmm.mciSendStringW(f"put rickvideo window at 0 0 {root_w} {root_h}", None, 0, 0)
    ctypes.windll.winmm.mciSendStringW("play rickvideo", None, 0, 0)

    def keep_top():
        root.lift()
        root.attributes('-topmost', True)
        root.after(200, keep_top)
    keep_top()

    root.bind("<Escape>", lambda e: "break")
    
    keyboard.add_hotkey('ctrl+alt+q', lambda: os.system(f"taskkill /f /pid {os.getpid()}"))

root = tk.Tk()
root.title("CRITICAL_ERROR")

total_width = root.winfo_vrootwidth()
total_height = root.winfo_vrootheight()
vroot_x = root.winfo_vrootx()
vroot_y = root.winfo_vrooty()

root.geometry(f"{total_width}x{total_height}+{vroot_x}+{vroot_y}")
root.attributes('-topmost', True)
root.configure(bg='#D32F2F')
root.overrideredirect(True)

keyboard.add_hotkey('ctrl+alt+q', secret_exit)
block_system_keys()
root.bind("<Escape>", lambda e: "break")

smiley_label = tk.Button(
    root, 
    text=":) ", 
    font=("Arial", 110), 
    fg="white", 
    bg="#D32F2F", 
    activeforeground="white", 
    activebackground="#D32F2F", 
    bd=0, 
    highlightthickness=0, 
    command=activate_rickroll
)
smiley_label.pack(anchor='w', padx=100, pady=(120, 20))

text_label = tk.Label(
    root, 
    text="Your PC ran into a hilarious problem and needs to be rickrolled.\n"
         "We're just collecting some funny info, and then you can restart.\n\n"
         "100% complete", 
    font=("Segoe UI", 22), justify="left", fg="white", bg="#D32F2F"
)
text_label.pack(anchor='w', padx=100)

support_label = tk.Label(root, text="Stop code: RICKROLL_DETECTED_HA_HA", font=("Segoe UI", 14), justify="left", fg="#FFCDD2", bg="#D32F2F")
support_label.pack(anchor='w', padx=100, pady=(30, 0))

secret_hint_label = tk.Label(
    root, 
    text="▲ System tip: try clicking on the smiley face to recover Windows files...", 
    font=("Segoe UI", 12, "italic"), 
    fg="#B71C1C", 
    bg="#D32F2F"
)
secret_hint_label.place(x=total_width - 550, y=total_height - 150)

root.mainloop()
