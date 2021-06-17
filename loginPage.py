import tkinter as tk
from PIL import Image, ImageTk


class LoginPage(tk.Frame):
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

		self.label_username = tk.Label(self.main_frame, text="Username", font=("Helvetica", 24, "bold"), bg="alice blue", fg="LightSteelBlue4")
		self.label_username.pack(pady=10)

		self.var_username = tk.StringVar()
		self.entry_username = tk.Entry(self.main_frame, font=("Helvetica", 20), textvariable=self.var_username)
		self.entry_username.pack(pady=10)

		self.label_password = tk.Label(self.main_frame, text="Password", font=("Helvetica", 24, "bold"), bg="alice blue", fg="LightSteelBlue4")
		self.label_password.pack(pady=10)

		self.var_password = tk.StringVar()
		self.entry_password = tk.Entry(self.main_frame, font=("Helvetica", 20), show="*", textvariable=self.var_password)
		self.entry_password.pack(pady=10)

		self.btn_login = tk.Button(self.main_frame, text="Login", font=("Monaco", 22, "bold"), command=lambda:self.app.auth_login())
		self.btn_login.pack(pady=10)

		self.btn_register = tk.Button(self.main_frame, text="Register", font=("Monaco", 22, "bold"), command=lambda:self.app.change_page('registerPage'))
		self.btn_register.pack(pady=10)