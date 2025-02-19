"""
Title: gui_customtk_basic.py
Created: 30 October 2024
Author: Clayton Bennett

Purpose:
Generate gui using customtkinter pypi package
"""
#import tkinter
import customtkinter as ctk

if True:
    ctk.set_appearance_mode("dark")
    #ctk.set_scaling(1.0)  # Adjust DPI scaling as needed
class App(ctk.CTk):
#class App(tkinter.Tk):
    cli_object = None
    @classmethod
    def pass_in_cli_object(cls,cli_object):
        cls.cli_object = cli_object
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.geometry("400x100")
        self.title("Pavlov 3D")
        self.grid_rowconfigure(3, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)
        #self.frame = ctk.CTkFrame(master=app)
            
            

        self.button = ctk.CTkButton(self, text="Run Main", command=self.button_main)
        #self.button.pack(padx=20, pady=20)
        #self.label.grid(row=0, column=0, padx=20)
        self.button.grid(row=1, column=1, padx=20, pady=10)

        self.button = ctk.CTkButton(self, text="Quit GUI", command=self.button_quit)
        #self.button.pack(padx=20, pady=20)
        #self.label.grid(row=0, column=0, padx=20)
        self.button.grid(row=1, column=2, padx=20, pady=10)
        
    def dummy_function(self):
        print("Function called")

    def button_main(self):
        print("button clicked: Run Main")
        self.cli_object.do_main(None)
    
    def button_quit(self):
        
        #self.protocol("WM_DELETE_WINDOW", self.destroy())
        #self.after_id = self.after(2000, self.dummy_function())
        #self.after_cancel(self.after_id)
        #self.after_cancel()
        self.destroy()
        #self.quit()
        print("GUI closed.")

if __name__ == "__main__":
    app = App()
    app.mainloop()