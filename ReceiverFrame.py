# Harsh Choudhary, 2103117

import tkinter as tk
from tkinter import ttk 
import customtkinter
from Receiver import Receiver
import threading
import time
from PIL import Image
import os

class ReceiverSide(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0,column=0,sticky="nsew")
        # self.thread_lock = threading.Lock()
        

    def create_widgets(self):
        # Widgets for the main screen
        self.recv_obj = Receiver(self.controller.final_field,self.controller.final_n,self.controller.final_k,self.controller.final_X,self.controller.final_systematic)
        self.finish = False
        self.finish_ok = False

        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=2)

        # Heading frame
        self.heading_label_frame = customtkinter.CTkFrame(self)
        self.heading_label_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")

        self.heading_label_frame.grid_rowconfigure(0,weight=1)
        self.heading_label_frame.grid_columnconfigure(0,weight=1)
        self.heading_label = customtkinter.CTkLabel(self.heading_label_frame,text="Receiver's Side\t",font=('HelVetica',24,'bold','underline'))
        self.heading_label.grid(row=0,column=0,sticky='nsew',pady = (10,15))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.heading_label_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=1, padx = 20, pady=(10, 10))

        # matrix frame
        self.matrix_frame = customtkinter.CTkFrame(self)
        self.matrix_frame.grid(row=1,column=0,sticky="nsew")

        self.matrix_frame.grid_rowconfigure(1,weight=1)
        self.matrix_frame.grid_columnconfigure(0,weight=1)
        self.blkmp_matrix_label = customtkinter.CTkLabel(self.matrix_frame,text="The Berlekamp Welch Algorithm",font=('Helvetica',14,'bold'))
        self.blkmp_matrix_label.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(60,20))
        # self.blkmp_matrix_textbox = customtkinter.CTkTextbox(self.matrix_frame,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'))
        self.populate_berlekamp_matrix()
        # self.blkmp_matrix_textbox.grid(row=1,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        # self.blkmp_matrix_textbox.configure(state="disabled")

        # answer frame
        self.ans_frame = customtkinter.CTkFrame(self)
        self.ans_frame.grid(row=1,column=1,sticky="nsew")

        self.ans_frame.grid_rowconfigure((1,3),weight=3)
        self.ans_frame.grid_rowconfigure(4,weight=1)
        self.ans_frame.grid_columnconfigure(0,weight=1)
        self.corrupted_codeword_label = customtkinter.CTkLabel(self.ans_frame,text="The corrupted codeword received is:",font=('Helvetica',13,'bold'),anchor='w')
        self.corrupted_codeword_label.grid(row=0,column=0,sticky='w',padx=(20,20),pady=(80,0))
        self.corrupted_codeword_textbox = customtkinter.CTkTextbox(self.ans_frame,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'),height=100)
        self.populate_corrupted_codeword()
        self.corrupted_codeword_textbox.grid(row=1,column=0,columnspan=2,sticky='nsew',padx=(20,20),pady=(5,20))
        self.corrupted_codeword_textbox.configure(state="disabled")
        self.decoded_message_label = customtkinter.CTkLabel(self.ans_frame,text="The decoded message is:",font=('Helvetica',13,'bold'),anchor='w')
        self.decoded_message_label.grid(row=2,column=0,sticky='w',padx=(20,20),pady=(20,0))
        self.decoded_message_textbox = customtkinter.CTkTextbox(self.ans_frame,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'),height=100)
        # self.populate_decoded_message()
        self.decoded_message_textbox.grid(row=3,column=0,columnspan=2,sticky='nsew',padx=(20,20),pady=(5,20))
        self.decoded_message_textbox.configure(state="disabled")
        self.progressbar = customtkinter.CTkProgressBar(self.ans_frame,mode='indeterminate')
        self.progressbar.grid(row=4,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.remark_textbox = customtkinter.CTkTextbox(self.ans_frame,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'),height=50)
        self.remark_textbox.configure(state="disabled")
        self.finish_button = customtkinter.CTkButton(self.ans_frame, border_width=2, command = self.finish_func,text="Finish")
        self.finish_button.grid(row=4,column=1,padx=(20,20),pady=(20,20),sticky='se')
        
        # self.recv_obj.decode(self.controller.codeword_corrupted)
        self.thread = threading.Thread(target=self.populate_decoded_message, daemon=True)
        self.thread.start()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)  

    def populate_berlekamp_matrix(self):
        # decoded_message = self.recv_obj.decode(self.controller.codeword_corrupted)
        # algorithm = "P(x): degree n-1 polynomial.\nSend P(1),...,P(n+2k)\nReceive R(1),...,R(n+2k)\nAt most k i's where P(i) != R(i).\nIdea:\nE(x) is error locator polynomial.\nRoot at each error point. Degree k.\nQ(x) = P(x)E(x) or degree n+k -1 polynomial.\nSet up system corresponding to Q(i) = R(i)E(i) where\nQ(x) is degree n+k -1 polynomial. Coefficients: a0,...,an+k-1\nE(x) is degree k polyonimal. Coefficients: b0,...,bk-1,1\nSolve. Then output P(x) = Q(x)/E(x)."
        # self.blkmp_matrix_textbox.insert(tk.END,algorithm)
        photo = customtkinter.CTkImage(light_image=Image.open(os.path.join("algo.png")),size=(360,400))
        content = customtkinter.CTkLabel(self.matrix_frame,image=photo,text="")
        content.grid(row=1,column=0,sticky='nsew',padx=(20,20),pady=(0,20))
        # source of image: https://www.youtube.com/watch?v=0WfAGR-vVwk
        


    def populate_corrupted_codeword(self):
        text = ""
        self.num_blocks = len(self.controller.codeword_corrupted)//self.recv_obj.n
        i=0
        while i<len(self.controller.codeword_corrupted):
            text += "[ "
            for j in range(self.recv_obj.n):
                text+=str(self.controller.codeword_corrupted[i])
                if j!=self.recv_obj.n-1:
                    text +=" "
                i+=1
            text+=" ]"
        # self.corrupted_codeword_textbox.configure(state='normal')  # Enable editing
        self.corrupted_codeword_textbox.delete(1.0, tk.END)  # Clear existing content
        self.corrupted_codeword_textbox.insert(tk.END, text)  # Insert new text
        # self.corrupted_codeword_textbox.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def populate_decoded_message(self):
        # print("called")
        self.progressbar.start()
        message = ""
        # print("Total decoded:",self.recv_obj.decode(self.controller.codeword_corrupted))
        for i in range(0,len(self.controller.codeword_corrupted),self.recv_obj.n):
            #print(f"block {i//self.recv_obj.n}")
            #print(f"codeword sent {self.controller.codeword_corrupted[i:i+self.recv_obj.n]}")
            m_decoded = self.recv_obj.decode_block(self.controller.codeword_corrupted[i:i+self.recv_obj.n])
            #print(m_decoded)
            if m_decoded[0]==-1:
                message += f"Error in block {i//self.recv_obj.n} could not be corrected!\n"
            text = "[ "
            for j in range(self.recv_obj.k):
                text+=str(m_decoded[j])
                if j!=self.recv_obj.k-1:
                    text +=" "
            # time.sleep(5)
            text+=" ]"
            self.decoded_message_textbox.configure(state='normal')
            self.decoded_message_textbox.insert(tk.END,text)
            self.decoded_message_textbox.configure(state='disabled')
            
        self.progressbar.stop()
        # print("out of loop")
        if message=="":
            message = "Successfully Decoded!"
        # self.progressbar.grid_forget()
        self.populate_remark(message,tk.END)

    def populate_remark(self,message,index):
        if message == "Successfully Decoded!":
            self.remark_textbox.configure(text_color = "green")
        else:
            self.remark_textbox.configure(text_color = "red")
        self.remark_textbox.configure(state='normal')
        self.remark_textbox.delete("1.0",tk.END)
        self.remark_textbox.insert(index,message)
        self.remark_textbox.configure(state='disabled')
        self.remark_textbox.grid(row=4,column=0,sticky='nsew',padx=(20,20),pady=(20,20))

    def finish_func(self):
        # self.progressbar.stop()
        # print("finish_pressed")
        self.populate_remark("Terminating all threads","1.0")
        self.controller.destroy()
# 1,2,2,1,5,2,5,6
