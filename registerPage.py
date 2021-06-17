import tkinter as tk
from PIL import Image, ImageTk


class RegisterPage(tk.Frame):
	
	def __init__(self, parent, App):
		
		self.app = App
		self.settings = App.settings

		super().__init__(parent)
		self.configure(bg="white")
		self.grid(row=0, column=0, sticky="nsew")
		parent.grid_columnconfigure(0, weight=1)
		parent.grid_rowconfigure(0, weight=1)


		#CREATE MAIN FRAME

		self.main_frame = tk.Frame(self, width=self.settings.width, height=self.settings.height, bg="blue")
		self.main_frame.pack(expand=True)

		#image = Image.open(self.settings.logo_path)
		#image_w, image_h = image.size
		#ratio = image_w/self.settings.side
		#image = image.resize((int(image_w//ratio),int(image_h//ratio)))

		#self.logo = ImageTk.PhotoImage(image)
		#self.label_logo = tk.Label(self.main_frame, image=self.logo)
		#self.label_logo.pack(padx=10, pady=10)

		self.label_register_username = tk.Label(self.main_frame, text="Username", font=("Helvetica", 24, "bold"), bg="alice blue", fg="LightSteelBlue4")
		self.label_register_username.pack(pady=10)

		self.var_register_username = tk.StringVar()
		self.entry_register_username = tk.Entry(self.main_frame, font=("Helvetica", 20), textvariable=self.var_register_username)
		self.entry_register_username.pack(pady=10)

		self.label_register_password = tk.Label(self.main_frame, text="Password", font=("Helvetica", 24, "bold"), bg="alice blue", fg="LightSteelBlue4")
		self.label_register_password.pack(pady=10)

		self.var_register_password = tk.StringVar()
		self.entry_register_password = tk.Entry(self.main_frame, font=("Helvetica", 20), textvariable=self.var_register_password)
		self.entry_register_password.pack(pady=10)

		self.btn_save_register = tk.Button(self.main_frame, text="Save", font=("Monaco", 22, "bold"), command=lambda:self.app.clicked_save_register_btn())
		self.btn_save_register.pack(pady=10)

		self.btn_cancel_register = tk.Button(self.main_frame, text="Cancel", font=("Monaco", 22, "bold"), command=lambda:self.app.create_loginPage())
		self.btn_cancel_register.pack(pady=10)
