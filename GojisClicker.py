import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time
import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Goji's Auto Clicker")
        self.root.geometry("350x400")
        self.root.configure(bg="black")  
        
        self.running = False
        self.interval = 1000  

        self.create_widgets()

        
        self.stop_key_thread = threading.Thread(target=self.listen_for_keys)
        self.stop_key_thread.daemon = True
        self.stop_key_thread.start()

    def create_widgets(self):
        
        self.interval_label = tk.Label(self.root, text="Click Interval (milliseconds):", fg="white", bg="black")
        self.interval_label.pack(pady=5)

        self.interval_entry = tk.Entry(self.root, fg="white", bg="black", insertbackground="white")
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "1000")

        self.update_interval_button = tk.Button(self.root, text="Update Interval", command=self.update_interval, bg="#555", fg="white")
        self.update_interval_button.pack(pady=5)

        self.position_label = tk.Label(self.root, text="Mouse Position (x, y):", fg="white", bg="black")
        self.position_label.pack(pady=5)

        self.position_entry = tk.Entry(self.root, fg="white", bg="black", insertbackground="white")
        self.position_entry.pack(pady=5)
        self.position_entry.insert(0, "0, 0")

        self.get_position_button = tk.Button(self.root, text="Get Mouse Position", command=self.get_mouse_position, bg="#555", fg="white")
        self.get_position_button.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Auto Clicker", command=self.start_autoclicker, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Auto Clicker", command=self.stop_autoclicker, bg="#F44336", fg="white")
        self.stop_button.pack(pady=5)

        
        self.message_label = tk.Label(self.root, text='Press "O" to stop the Autoclicker and press "P" to get location!', font=("Copperplate Gothic", 10), fg="white", bg="black")
        self.message_label.pack(side=tk.BOTTOM, pady=10)

    def get_mouse_position(self):
        x, y = pyautogui.position()
        self.position_entry.delete(0, tk.END)
        self.position_entry.insert(0, f"{x}, {y}")

    def update_interval(self):
        try:
            self.interval = float(self.interval_entry.get()) / 1000.0  
            if self.running:
                messagebox.showinfo("Interval Updated", f"Click interval updated to {self.interval * 1000} milliseconds.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the interval.")

    def start_autoclicker(self):
        try:
            self.interval = float(self.interval_entry.get()) / 1000.0  
            position = tuple(map(int, self.position_entry.get().split(', ')))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for interval and position.")
            return

        self.running = True
        self.position = position
        self.click_thread = threading.Thread(target=self.autoclick)
        self.click_thread.start()

    def autoclick(self):
        while self.running:
            pyautogui.click(self.position)
            time.sleep(self.interval)

    def stop_autoclicker(self):
        self.running = False
        if hasattr(self, 'click_thread') and self.click_thread.is_alive():
            self.click_thread.join()

    def listen_for_keys(self):
        while True:
            if keyboard.is_pressed('o'):
                self.stop_autoclicker()
            if keyboard.is_pressed('p'):
                self.get_mouse_position()
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()