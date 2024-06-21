# Harsh Choudhary, 2103117

import tkinter as tk
import customtkinter
from SenderFrame import SenderSide
from EnvironmentFrame import EnvironmentSide
from ReceiverFrame import ReceiverSide
import ctypes

class RSWelcome(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Reed Solomon Codes')
        self.configure(background='cyan')

        self.geometry(f"{1100}x{580}")
        # self.resizable(0,0)
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # Create a container to hold all the screens
        self.container = tk.Frame(self,background='orange')
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.codeword = None
        self.codeword_tilde = None
        self.frames = {}  # Dictionary to hold all screens
        

        # Create and add the sender screen
        sender_frame = SenderSide(self.container, self)
        self.frames[SenderSide] = sender_frame
        # sender_frame.grid(row=0, column=0, sticky="nsew")

        # # Create and add the env screen
        env_frame = EnvironmentSide(self.container, self)
        self.frames[EnvironmentSide] = env_frame
        # env_frame.grid(row=0, column=0, sticky="nsew")

        # # Create and add the receiver screen
        receiver_frame = ReceiverSide(self.container, self)
        self.frames[ReceiverSide] = receiver_frame
        # receiver_frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the Sender screen initially
        self.show_frame(SenderSide)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    
    # try:
    #     x11 = ctypes.cdll.LoadLibrary("libX11.so")
    #     x11.XInitThreads()
    # except Exception as e:
    #     print("Failed to initialize Xlib threads support:", e)
    
    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    app = RSWelcome()
    app.mainloop()
