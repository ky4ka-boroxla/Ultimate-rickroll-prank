# учился пайтону пока это писал
import tkinter as tk
import os
import sys
import ctypes
import keyboard

def resource_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

VIDEO_PATH = resource_path("rick.avi")
VIDEO_DURATION_MS = 213000

def mci(command: str) -> str:
    buf = ctypes.create_unicode_buffer(512)
    err = ctypes.windll.winmm.mciSendStringW(command, buf, 512, 0)
    if err:
        err_buf = ctypes.create_unicode_buffer(256)
        ctypes.windll.winmm.mciGetErrorStringW(err, err_buf, 256)
        print(f"MCI error {err}: {err_buf.value} | cmd: {command}")
    return buf.value

def block_system_keys():
    keyboard.block_key('left windows')
    keyboard.block_key('right windows')
    keyboard.add_hotkey('alt+tab', lambda: None, suppress=True)
    keyboard.add_hotkey('ctrl+esc', lambda: None, suppress=True)
    keyboard.add_hotkey('alt+f4', lambda: None, suppress=True)

def clean_exit(event=None):
    try:
        keyboard.unblock_key('left windows')
        keyboard.unblock_key('right windows')
        keyboard.remove_all_hotkeys()
    except Exception:
        pass

    try:
        mci("stop rickvideo")
        mci("close rickvideo")
    except Exception:
        pass

    try:
        root.destroy()
    except Exception:
        pass

    sys.exit(0)

def activate_rickroll():
    for widget in (smiley_label, text_label, support_label, secret_hint_label):
        try:
            widget.destroy()
        except Exception:
            pass

    root.configure(bg='black')
    root.config(cursor="no")

    hwnd = root.winfo_id()
    open_cmd = f'open "{VIDEO_PATH}" type mpegvideo alias rickvideo style child parent {hwnd}'
    mci(open_cmd)

    ctypes.windll.user32.SetProcessDPIAware()
    screen_w = ctypes.windll.user32.GetSystemMetrics(0)
    screen_h = ctypes.windll.user32.GetSystemMetrics(1)

    mci(f"put rickvideo window at 0 0 {screen_w} {screen_h}")
    mci("play rickvideo")

    def keep_top():
        try:
            root.lift()
            root.attributes('-topmost', True)
            root.after(400, keep_top)
        except Exception:
            pass
    keep_top()

    root.after(VIDEO_DURATION_MS + 1500, clean_exit)
    keyboard.add_hotkey('ctrl+alt+q', clean_exit)

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

keyboard.add_hotkey('ctrl+alt+q', clean_exit)
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

support_label = tk.Label(
    root,
    text="Stop code: RICKROLL_DETECTED_HA_HA",
    font=("Segoe UI", 14), justify="left", fg="#FFCDD2", bg="#D32F2F"
)
support_label.pack(anchor='w', padx=100, pady=(30, 0))

secret_hint_label = tk.Label(
    root,
    text="▲ System tip: try clicking on the smiley face to recover Windows files...",
    font=("Segoe UI", 12, "italic"),
    fg="#B71C1C",
    bg="#D32F2F"
)
secret_hint_label.place(x=total_width - 550, y=total_height - 150)

root.protocol("WM_DELETE_WINDOW", clean_exit)

root.mainloop()
