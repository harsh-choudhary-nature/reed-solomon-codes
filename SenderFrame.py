# Harsh Choudhary, 2103117
import tkinter as tk
import customtkinter
from EnvironmentFrame import EnvironmentSide
from Sender import Sender
from FiniteField import Zq
from utils import is_prime,to_list

class SenderSide(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0,column=0,sticky="nsew")
        self.sender_obj = self.create_sender_obj()
        self.sender_obj.field.q = -1
        self.sender_obj.k = -1
        self.create_widgets()
    
    def create_widgets(self):

        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure((0,1),weight=1)

        # Label of Sender's Side
        self.heading_label_frame = customtkinter.CTkFrame(self)
        self.heading_label_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")

        self.heading_label_frame.grid_rowconfigure(0,weight=1)
        self.heading_label_frame.grid_columnconfigure(0,weight=1)
        self.heading_label = customtkinter.CTkLabel(self.heading_label_frame,text="Sender's Side\t",font=('HelVetica',24,'bold','underline'))
        self.heading_label.grid(row=0,column=0,sticky='nsew',pady = (10,15))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.heading_label_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=1, padx = 20, pady=(10, 10))        

        # set parameters of the code
        self.parameters_frame = customtkinter.CTkFrame(self)
        self.parameters_frame.grid(row=1,column=0,sticky="nsew")

        self.parameters_frame.grid_rowconfigure(5,weight=1)
        self.parameters_frame.grid_columnconfigure((0,1),weight=1)

        self.q_entry = customtkinter.CTkEntry(self.parameters_frame,placeholder_text="Field Size (q)")
        self.q_entry.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(60,20))
        self.q_entry.bind("<KeyRelease>",self.q_entry_update)
        self.default_entry_border_color = self.q_entry.cget("border_color")
        self.q_entry_warning_label = customtkinter.CTkLabel(self.parameters_frame,text_color="red",anchor='w')
        # self.q_entry_warning_label.grid(row=0,column=1,columnspan=2,sticky='nsew',pady=(60,20))
        self.k_entry = customtkinter.CTkEntry(self.parameters_frame,placeholder_text="Message Block Length (k)")
        self.k_entry.grid(row=1,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.k_entry.bind("<KeyRelease>",self.k_entry_update)
        self.k_entry_warning_label = customtkinter.CTkLabel(self.parameters_frame,text_color="red",anchor='w')
        # self.k_entry_warning_label.grid(row=1,column=1,columnspan=2,sticky='nsew')
        self.n_entry = customtkinter.CTkEntry(self.parameters_frame,placeholder_text="Codeword Block Length (n)")
        self.n_entry.grid(row=2,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.n_entry.bind("<KeyRelease>",self.n_entry_update)
        self.n_entry_warning_label = customtkinter.CTkLabel(self.parameters_frame,text_color="red",anchor='w')
        # self.n_entry_warning_label.grid(row=2,column=1,columnspan=2,sticky='nsew')
        self.d_entry = customtkinter.CTkTextbox(self.parameters_frame,height=0,border_width=2,fg_color='transparent')
        self.d_entry.grid(row=3,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.d_entry.insert(tk.END,"Distance (d)")
        self.d_entry.configure(state="disabled")
        self.systematic_check = customtkinter.CTkCheckBox(self.parameters_frame,text='Systematic')
        self.systematic_check.grid(row=3,column=1,sticky='w')
        self.systematic_check.bind("<Button-1>",self.systematic_checkbox_update)
        self.M_entry_label = customtkinter.CTkLabel(self.parameters_frame,text="Enter the Message 'M' (comma or space separated) (must be a multiple of k):-",anchor='w')
        self.M_entry_label.grid(row=4,column=0,padx=(20,20),pady=(20,0),sticky='nsew')
        self.M_entry = customtkinter.CTkTextbox(self.parameters_frame,border_width=2)
        self.M_entry.grid(row=5,column=0,sticky='nsew',padx=(20,20),pady=(5,20),rowspan=2)
        # self.M_entry.bind("<KeyRelease>",self.M_entry_update)
        self.M_entry_warning_label = customtkinter.CTkLabel(self.parameters_frame,text_color="red",anchor='w')
        # self.M_entry_warning_label.grid(row=5,column=1,sticky='nsew')
        self.send_button = customtkinter.CTkButton(self.parameters_frame, border_width=2, command = self.validate_everything,text="Send")
        self.send_button.grid(row=6,column=1,padx=(0,20),pady=(20,20),sticky='ew')


        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=1,column=1,sticky='nsew')

        self.info_frame.grid_columnconfigure(0,weight=1)
        # self.info_frame.grid_rowconfigure((0,1),weight=1)
        self.info_frame.grid_rowconfigure(1,weight=1)

        self.points = customtkinter.CTkTextbox(self.info_frame,height=100,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'))
        self.points.insert("0.0",text="The evaluation points are:-")
        self.points.grid(row=0,column=0,sticky='nsew',padx=(20,20),pady=(60,20))
        self.points.configure(state="disabled")
        self.G = customtkinter.CTkTextbox(self.info_frame,border_width=2,fg_color='transparent',font=('Helvetica',12,'bold'))
        self.G.insert(tk.END,text="The Generator Matrix G (for usual RS code) is:-\n\n")
        self.G.grid(row=1,column=0,sticky='nsew',padx=(20,20),pady=(20,20))
        self.G.configure(state="disabled")
    
    def create_sender_obj(self):
        return Sender(Zq(7),4)
    
    def q_entry_update(self,event):
        try:
            q_entered = int(self.q_entry.get())
            if not is_prime(q_entered):
                # display warning 
                self.q_entry_warning_label.configure(text="Field size must be prime")
                self.q_entry_warning_label.grid(row=0,column=1,sticky='nsew',pady=(60,20))
                self.q_entry.configure(border_color="red")
                self.empty_d()
                self.empty_points()
                self.empty_G()
            else:
                self.sender_obj.field = Zq(q_entered)
                self.q_entry.configure(border_color=self.default_entry_border_color)
                self.q_entry_warning_label.grid_forget()
                try:
                    if self.is_valid(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get())):
                        self.fill_d(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get()))
                        self.update_points()
                        self.update_G()
                        self.k_entry_warning_label.grid_forget()
                        self.k_entry.configure(border_color=self.default_entry_border_color)
                        self.n_entry_warning_label.grid_forget()
                        self.n_entry.configure(border_color=self.default_entry_border_color)
                    else:
                        raise ValueError
                except ValueError:
                    self.empty_d()
                    self.empty_points()
                    self.empty_G()
        except ValueError:
            self.empty_d()
            self.empty_points()
            self.empty_G()
            if not len(self.q_entry.get())==0:
                self.q_entry_warning_label.configure(text="Invalid Field Size")
                self.q_entry_warning_label.grid(row=0,column=1,sticky='nsew',pady=(60,20))
                self.q_entry.configure(border_color="red")


    def k_entry_update(self,event):
        try:
            k_entered = int(self.k_entry.get())
            if k_entered>0:
                self.sender_obj.k = k_entered
                self.k_entry.configure(border_color=self.default_entry_border_color)
                self.k_entry_warning_label.grid_forget()
                try:
                    if self.is_valid(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get())):
                        self.fill_d(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get()))
                        self.update_points()
                        self.update_G()
                        self.q_entry.configure(border_color=self.default_entry_border_color)
                        self.q_entry_warning_label.grid_forget()
                        self.n_entry.configure(border_color=self.default_entry_border_color)
                        self.n_entry_warning_label.grid_forget()
                    else:
                        raise ValueError
                except ValueError:
                    self.empty_d()
                    self.empty_points()
                    self.empty_G()
            else:
                raise ValueError
        except ValueError:
            self.empty_d()
            self.empty_points()
            self.empty_G()
            if not len(self.k_entry.get())==0:
                self.k_entry_warning_label.configure(text="Invalid k")
                self.k_entry_warning_label.grid(row=1,column=1,sticky='nsew',pady=(20,20))
                self.k_entry.configure(border_color="red")

    def n_entry_update(self,event):
        try:
            n_entered = int(self.n_entry.get())
            if n_entered>0:
                self.sender_obj.n = n_entered
                self.n_entry.configure(border_color=self.default_entry_border_color)
                self.n_entry_warning_label.grid_forget()
                try:
                    if self.is_valid(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get())):
                        self.fill_d(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get()))
                        self.update_points()
                        self.update_G()
                        self.q_entry.configure(border_color=self.default_entry_border_color)
                        self.q_entry_warning_label.grid_forget()
                        self.k_entry.configure(border_color=self.default_entry_border_color)
                        self.k_entry_warning_label.grid_forget()
                    else:
                        raise ValueError
                except ValueError:
                    self.empty_d()
                    self.empty_points()
                    self.empty_G()
            else:
                raise ValueError
        except ValueError:
            self.empty_d()
            self.empty_points()
            self.empty_G()
            if not len(self.n_entry.get())==0:
                self.n_entry_warning_label.configure(text="Invalid n")
                self.n_entry_warning_label.grid(row=2,column=1,sticky='nsew',pady=(20,20))
                self.n_entry.configure(border_color="red")
        
    def M_entry_label_update(self):
        try:
            # print("Validating",self.q_entry.get(),self.k_entry.get(),self.n_entry.get())
            # print(self.M_entry.get("1.0",tk.END),type(self.M_entry.get("1.0",tk.END)))
            k_entered = int(self.k_entry.get())
            q_entered = int(self.q_entry.get())
            # print("Reached")
            M_entered = to_list(self.M_entry.get("1.0",tk.END),set([","," ","\n","\t",".",";",":"]))
            # print(M_entered)
            # print(M_entered,type(M_entered))
            for i in range(len(M_entered)):
                if len(M_entered[i])>=2 and M_entered[i][0]=="0" and M_entered[i][1]=="0":
                    raise ValueError
                M_entered[i] = int(M_entered[i])
                if M_entered[i]<0 or M_entered[i]>=q_entered:
                    raise ValueError
            if len(M_entered)%k_entered!=0:
                raise ValueError
            # print(M_entered,"returning True")
            return True
        except ValueError:
            return False

    def is_valid(self,q,k,n):
        return is_prime(q) and q>=n and n>=k

    def fill_d(self,q,k,n):
        # update d
        self.d_entry.configure(state='normal')  # Enable editing
        self.d_entry.delete(1.0, tk.END)  # Clear existing content
        self.d_entry.insert(tk.END, str(n-k+1))  # Insert new text
        self.d_entry.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()
    
    def empty_d(self):
        self.d_entry.configure(state='normal')  # Enable editing
        self.d_entry.delete(1.0, tk.END)  # Clear existing content
        self.d_entry.insert(tk.END, "Distance (d)")  # Insert new text
        self.d_entry.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def update_points(self):
        points = self.sender_obj.get_evaluation_points()
        text_to_enter = "The evaluation points are:-\n\n"
        for point in points:
            text_to_enter += str(point)+"\t"

        self.points.configure(state='normal')  # Enable editing
        self.points.delete(1.0, tk.END)  # Clear existing content
        self.points.insert(tk.END, text_to_enter)  # Insert new text
        self.points.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def empty_points(self):
        text_to_enter = "The evaluation points are:-\n\n"
        self.points.configure(state='normal')  # Enable editing
        self.points.delete(1.0, tk.END)  # Clear existing content
        self.points.insert(tk.END, text_to_enter)  # Insert new text
        self.points.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def update_G(self):
        text_to_enter = "The Generator Matrix G (for usual RS code) is:-\n\n"
        G = self.sender_obj.get_generator_matrix()
        for i in range(len(G)):
            for j in range(len(G[i])):
                text_to_enter += str(G[i][j])+"\t"
            text_to_enter+="\n\n"

        self.G.configure(state='normal')  # Enable editing
        self.G.delete(1.0, tk.END)  # Clear existing content
        self.G.insert(tk.END, text_to_enter)  # Insert new text
        self.G.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def empty_G(self):
        text_to_enter = "The Generator Matrix G (for usual RS code) is:-\n\n"
        self.G.configure(state='normal')  # Enable editing
        self.G.delete(1.0, tk.END)  # Clear existing content
        self.G.insert(tk.END, text_to_enter)  # Insert new text
        self.G.configure(state='disabled')  # Disable editing
        # Update the UI by processing all pending events
        self.controller.update_idletasks()

    def systematic_checkbox_update(self,event):
        self.sender_obj.systematic = bool(self.systematic_check.get())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)        

    def validate_everything(self):
        if self.M_entry_label_update():
            self.M_entry.configure(border_color=self.default_entry_border_color)
            self.M_entry_warning_label.grid_forget()
            try:
                if self.is_valid(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get())):
                    self.fill_d(int(self.q_entry.get()),int(self.k_entry.get()),int(self.n_entry.get()))
                    self.q_entry.configure(border_color=self.default_entry_border_color)
                    self.q_entry_warning_label.grid_forget()
                    self.k_entry.configure(border_color=self.default_entry_border_color)
                    self.k_entry_warning_label.grid_forget()
                    self.n_entry.configure(border_color=self.default_entry_border_color)
                    self.n_entry_warning_label.grid_forget()
                    self.update_points()
                    self.update_G()
                    
                    # just being double sure to pick correct values
                    self.sender_obj.field = Zq(int(self.q_entry.get()))
                    self.sender_obj.k = int(self.k_entry.get())
                    self.sender_obj.n = int(self.n_entry.get())
                    self.sender_obj.d = self.sender_obj.n - self.sender_obj.k + 1
                    self.sender_obj.systematic = bool(self.systematic_check.get())

                    M = to_list(self.M_entry.get("1.0",tk.END),set([","," ","\n","\t",".",";",":"]))
                    self.move_to_next_frame([int(elem) for elem in M])
                else:
                    raise ValueError
            except ValueError:
                self.empty_d()
                self.empty_points()
                self.empty_G()
                # show warning for individual boxes
                try:
                    q_entered = int(self.q_entry.get())
                    if not is_prime(q_entered):
                        raise ValueError

                    try:
                        k_entered = int(self.k_entry.get())
                        if k_entered<=0 or k_entered>q_entered:
                            raise ValueError

                        try:
                            n_entered = int(self.n_entry.get())
                            if n_entered<=0 or n_entered<k_entered or n_entered > q_entered:
                                raise ValueError
                        except ValueError:
                            # value error for n
                            self.n_entry_warning_label.configure(text="Invalid n")
                            self.n_entry_warning_label.grid(row=2,column=1,sticky='nsew',pady=(20,20))
                            self.n_entry.configure(border_color="red")
                            self.empty_d()
                            self.empty_points()
                            self.empty_G()    
                    except ValueError:
                        # value error for k
                        self.k_entry_warning_label.configure(text="Invalid k")
                        self.k_entry_warning_label.grid(row=1,column=1,sticky='nsew',pady=(20,20))
                        self.k_entry.configure(border_color="red")
                        self.empty_d()
                        self.empty_points()
                        self.empty_G()
                except ValueError:
                    # value error for q_entry
                    self.q_entry_warning_label.configure(text="Invalid Field Size")
                    self.q_entry_warning_label.grid(row=0,column=1,sticky='nsew',pady=(60,20))
                    self.q_entry.configure(border_color="red")
                    self.empty_d()
                    self.empty_points()
                    self.empty_G()

        else:
            self.M_entry_warning_label.configure(text="Message length must be a multiple of k\nIt should contain only \nsymbols from finite field")
            self.M_entry_warning_label.grid(row=5,column=1,sticky='nsew',pady=(20,20))
            self.M_entry.configure(border_color="red")
                        
    def move_to_next_frame(self,message):
        self.controller.codeword = self.sender_obj.encode(message)
        self.controller.final_n = self.sender_obj.n
        self.controller.final_k = self.sender_obj.k
        self.controller.final_d = self.sender_obj.d
        self.controller.final_X = self.sender_obj.get_evaluation_points()
        self.controller.final_field = self.sender_obj.field
        self.controller.final_systematic = self.sender_obj.systematic
        
        # print("codeword in sender_frame",self.controller.codeword)
        self.controller.frames[EnvironmentSide].create_widgets()
        self.controller.show_frame(EnvironmentSide)
