# Harsh Choudhary, 2103117

import tkinter as tk
from tkinter import ttk 
from ReceiverFrame import ReceiverSide
import customtkinter
from Environment import Environment

class EnvironmentSide(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0,column=0,sticky="nsew")

    def create_widgets(self):
        self.env_obj = self.create_environment_obj()
        self.codeword = self.controller.codeword
        # print(self.codeword)
        
        self.grid_rowconfigure((1,4),weight=1)
        self.grid_columnconfigure(0,weight=1)

        # Label of Sender's Side
        self.heading_label_frame = customtkinter.CTkFrame(self)
        self.heading_label_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")

        self.heading_label_frame.grid_rowconfigure(0,weight=1)
        self.heading_label_frame.grid_columnconfigure(0,weight=1)
        self.heading_label = customtkinter.CTkLabel(self.heading_label_frame,text="Channel (Add Noise)\t",font=('HelVetica',24,'bold','underline'))
        self.heading_label.grid(row=0,column=0,sticky='nsew',pady = (10,15))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.heading_label_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=1, padx = 20, pady=(10, 10))

        # add the codeword textbox frame
        self.codeword_textbox_frame = customtkinter.CTkFrame(self)
        self.codeword_textbox_frame.grid(row=1,column=0,sticky="nsew",columnspan=2)

        self.codeword_textbox_frame.grid_rowconfigure(0,weight=1)
        self.codeword_textbox_frame.grid_columnconfigure(0,weight=1)

        self.codeword_textbox = customtkinter.CTkTextbox(self.codeword_textbox_frame,height=100,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'))
        self.codeword_textbox.insert(tk.END,self.getCodewordText(self.codeword))
        self.codeword_textbox.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(60,20))
        self.codeword_textbox.configure(state="disabled")

        # add the error control frame
        self.error_control_frame = customtkinter.CTkFrame(self)
        self.error_control_frame.grid(row=2,column=0,sticky="nsew",columnspan=2)

        self.error_control_frame.grid_rowconfigure(0,weight=1)
        self.error_control_frame.grid_columnconfigure(0,weight=4)
        self.error_control_frame.grid_columnconfigure(2,weight=1)

        self.error_slider = customtkinter.CTkSlider(self.error_control_frame, from_=0, to=self.env_obj.n, number_of_steps=self.env_obj.n,progress_color='red',command=self.update_labels)
        self.error_slider.set(0)
        self.error_slider_btn_color = self.error_slider.cget("button_color")
        self.error_slider.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.error_slider_label = customtkinter.CTkLabel(self.error_control_frame,text="0"+" errors per block", font=('Helvetica',12,'bold'))
        self.error_slider_label.grid(row=0,column=1,padx=(0,20),pady=(20,20))
        self.error_slider_comment = customtkinter.CTkLabel(self.error_control_frame,text="\tThese errors can be corrected!", font=('Helvetica',12,'bold'),text_color="green",anchor='e')
        self.error_slider_comment.grid(row=0,column=2,padx=(0,20),pady=(20,20),sticky='nsew')
        
        # add the randomise frame
        self.randomise_frame = customtkinter.CTkFrame(self)
        self.randomise_frame.grid(row=3,column=0,sticky="nsew",columnspan=2)

        self.randomise_frame.grid_rowconfigure(0,weight=1)
        # self.randomise_frame.grid_columnconfigure(0,weight=4)
        self.randomise_frame.grid_columnconfigure(2,weight=1)

        self.randomise_label = customtkinter.CTkLabel(self.randomise_frame,text="Randomise errors (may cause undetected errors):",font=('Helvetica',12,"bold"))
        self.randomise_label.grid(row=0,column=0,sticky='nsew',padx=(20,0),pady=(20,20))
        self.randomise_switch = customtkinter.CTkSwitch(self.randomise_frame,command=self.change_error_type,text="")
        self.randomise_switch_state = False
        self.randomise_switch.grid(row=0,column=1,sticky='nsew',padx=(5,20),pady=(20,20))
        
        # add the corrupted codeword frame
        self.corrupted_codeword_textbox_frame = customtkinter.CTkFrame(self)
        self.corrupted_codeword_textbox_frame.grid(row=4,column=0,sticky="nsew",columnspan=2)

        self.corrupted_codeword_textbox_frame.grid_rowconfigure(0,weight=1)
        self.corrupted_codeword_textbox_frame.grid_columnconfigure(0,weight=1)

        self.corrupted_codeword_textbox = customtkinter.CTkTextbox(self.corrupted_codeword_textbox_frame,height=100,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'))
        self.getCorruptedCodewordText(self.codeword)
        self.corrupted_codeword_textbox.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(60,20))
        self.corrupted_codeword_textbox.configure(state="disabled")
        self.proceed_button = customtkinter.CTkButton(self.corrupted_codeword_textbox_frame, border_width=2, command = self.open_receiver_side,text="Proceed")
        self.proceed_button.grid(row=1,column=0,padx=(20,20),pady=(20,20),sticky='e')


    def create_environment_obj(self):
        return Environment(self.controller.final_n,self.controller.final_k,self.controller.final_field,self.controller.final_X)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)  

    def getCodewordText(self,C_list):
        ans = "The codeword is:-\n\n"
        i=0
        while i<len(C_list):
            ans += "[ "
            for j in range(self.env_obj.n):
                ans+=str(C_list[i])
                if j!=self.env_obj.n-1:
                    ans+=" "
                i+=1
            ans += " ]"
        return ans
    
    def get_max_errors(self,n,k):
        d = n-k+1
        return (d-1)//2
    
    def change_error_type(self):
        self.randomise_switch_state = not self.randomise_switch_state
        if self.randomise_switch_state:
            self.error_slider_fg_color = self.error_slider.cget("fg_color")
            self.error_slider.configure(state="disabled",button_color="gray",fg_color="gray",progress_color="gray")
            self.error_slider_comment_color = self.error_slider_comment.cget("text_color")
            self.error_slider_comment.configure(text_color="gray")
            self.env_obj.max_errors = self.get_max_errors(self.env_obj.n,self.env_obj.k)
            self.env_obj.randomise = True
            self.getCorruptedCodewordText(self.codeword)
        else:
            self.error_slider.configure(state="normal",button_color=self.error_slider_btn_color,fg_color=self.error_slider_fg_color,progress_color="red")
            self.error_slider_comment.configure(text_color=self.error_slider_comment_color)
            self.env_obj.max_errors = int(self.error_slider.get())
            self.env_obj.randomise = False
            self.getCorruptedCodewordText(self.codeword)

    def update_labels(self,value):
        self.error_slider_label.configure(text=str(int(value))+" errors per block")
        self.env_obj.max_errors = int(value)
        if value > self.get_max_errors(self.env_obj.n,self.env_obj.k):
            # print("Uncorrectable")
            self.error_slider_comment.configure(text="\tThis high error can't be corrected!",text_color="red")
        else:
            self.error_slider_comment.configure(text="\tThese errors can be corrected!",text_color="green")
        
        self.getCorruptedCodewordText(self.codeword)

    def getCorruptedCodewordText(self,C_list):
        self.corrupted_codeword_textbox.configure(state='normal')  # Enable editing
        self.corrupted_codeword_textbox.delete(1.0, tk.END)  # Clear existing content

        ans = "The corrupted codeword is:-\n\n"
        self.corrupted_codeword_textbox.insert(tk.END,ans)
        C_list_tilde = self.env_obj.err(C_list)
        i=0
        while i<len(C_list_tilde):
            self.corrupted_codeword_textbox.insert(tk.END,"[ ")
            for j in range(self.env_obj.n):
                # ans+=str(C_list_tilde[i])
                if C_list_tilde[i]!=C_list[i]:
                    self.corrupted_codeword_textbox.tag_config("color_change",foreground="red")
                    self.corrupted_codeword_textbox.insert(tk.END,str(C_list_tilde[i])+" ","color_change")
                else:
                    # self.corrupted_codeword_textbox.tag_config("normal_color",foreground="black")
                    self.corrupted_codeword_textbox.insert(tk.END,str(C_list_tilde[i])+" ","normal_color")
                i+=1
            self.corrupted_codeword_textbox.insert(tk.END," ]")
        self.controller.codeword_corrupted = C_list_tilde
        self.corrupted_codeword_textbox.configure(state='disabled')  # Disable editing
        self.controller.update_idletasks()

    # def getCorruptedCodewordText(self,C_list):
    #     self.corrupted_codeword_textbox.configure(state='normal')  # Enable editing
    #     self.corrupted_codeword_textbox.delete(1.0, tk.END)  # Clear existing content

    #     ans = "The corrupted codeword is:-\n\n"
    #     # self.corrupted_codeword_textbox.tag_add("color_change",f"1.0",f"1.5")
    #     # self.corrupted_codeword_textbox.insert(tk.END,ans)
    #     C_list_tilde = self.env_obj.err(C_list)
    #     line = 3
    #     i=0
    #     tag_index =0
    #     while i<len(C_list_tilde):
    #         # self.corrupted_codeword_textbox.insert(tk.END,"[ ")
    #         ans += "[ "
    #         tag_index += 2
    #         for j in range(self.env_obj.n):
    #             # ans+=str(C_list_tilde[i])
    #             if C_list_tilde[i]!=C_list[i]:
    #                 index = f"{line}.{tag_index}"
    #                 print(f"index: {index}")
    #                 # self.corrupted_codeword_textbox.tag_add("color_change",f"3.{tag_index}",f"3.{tag_index}+{len(str(C_list_tilde[i]))}c")
    #                 self.corrupted_codeword_textbox.tag_add("color_change",index, f"{index}+{len(str(C_list_tilde[i]))}c")
    #                 # print("reached",tag_index,i)
    #                 ans += str(C_list_tilde[i]) + " "
    #                 tag_index += len(str(C_list_tilde[i]))+1
    #             else:
    #                 # self.corrupted_codeword_textbox.tag_config("color_change",f"3.{tag_index}",f"3.{tag_index+len(C_list_tilde[i])}")
    #                 ans += str(C_list_tilde[i])+" "
    #                 tag_index += len(str(C_list_tilde[i]))+1
    #                 # self.corrupted_codeword_textbox.tag_add("no_color_change",f"3.{tag_index}",f"3.{tag_index}+{len(str(C_list_tilde[i]))}c")
    #             i+=1
    #         # self.corrupted_codeword_textbox.insert(tk.END," ]")
    #         ans += " ]"
    #         tag_index +=2
    #     self.controller.codeword_corrupted = C_list_tilde
    #     self.corrupted_codeword_textbox.insert(tk.END,ans)

    #     self.corrupted_codeword_textbox.tag_config("color_change",foreground="red")
    #     # self.corrupted_codeword_textbox.tag_config("no_color_change",foreground="black")
    #     self.corrupted_codeword_textbox.configure(state='disabled')  # Disable editing
    #     self.controller.update_idletasks()


    def open_receiver_side(self):
        # self.controller.codeword_corrupted = self.sender_obj.encode(message) # done already
        # self.controller.final_n = self.sender_obj.n
        # self.controller.final_k = self.sender_obj.k
        # self.controller.final_d = self.sender_obj.d
        # self.controller.final_X = self.sender_obj.get_evaluation_points()
        # self.controller.final_field = self.sender_obj.field
        
        # print("codeword in sender_frame",self.controller.codeword)
        self.controller.frames[ReceiverSide].create_widgets()
        self.controller.show_frame(ReceiverSide)

'''
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
1,2,2,1,5,2,5,6
'''
