import sys

import tkinter as tk
from tkinter import messagebox as msg

from settings import Settings
from appPage import AppPage
from loginPage import LoginPage
from registerPage import RegisterPage

class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable(0,0)

		self.create_container()
		self.create_menus()

		self.pages = {}
		self.create_appPage()
		self.create_registerPage()
		self.create_loginPage()

	def create_loginPage(self):
		self.pages['loginPage'] = LoginPage(self.container, self)
		self.menuBar.delete("File")

	def create_registerPage(self):
		self.pages['registerPage'] = RegisterPage(self.container, self)

	def auth_login(self):
		username = self.pages['loginPage'].var_username.get()
		password = self.pages['loginPage'].var_password.get()


		granted = self.settings.login(username, password)
		if granted:
			self.change_page('appPage')
			self.create_menus()

	def change_page(self, page):
		page = self.pages[page]
		page.tkraise()

	def create_menus(self):
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		#addNew = AppPage(self, container)
		#self.fileMenu.add_command(label="New Item", command=self.addNew.clicked_add_new_btn)
		self.fileMenu.add_command(label="Log Out", command=self.create_loginPage)
		self.fileMenu.add_command(label="Exit", command=self.exit_program)

		self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label="About", command=self.show_about_info)

		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)


	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)


	def create_appPage(self):
		self.pages['appPage'] = AppPage(self.container, self.app)


	def show_about_info(self):
		msg.showinfo("About Contact App", "App made by Olivia The and Saori Nariko Chen.\nDibantu kelompok Fioreno Malvin juga sih sir hehe\n17 juni 2021, update button works")
		#msg.showwarning("About Contact App", "This apps created by\n1. Ali\n2. Budi\n\nCopyright-2021")
		#msg.showerror("About Contact App", "This apps created by\n1. Ali\n2. Budi\n\nCopyright-2021")

	def clicked_save_register_btn(self):
		confirm = msg.askyesnocancel('Save Confirmation', 'Are you sure to register this account?')
			
		if confirm:
			registered_username = self.pages['registerPage'].var_register_username.get()
			registered_password = self.pages['registerPage'].var_register_password.get()

			if registered_username in self.settings.users:
				msg.showerror("Registration Error", "Username already exists")
				self.create_registerPage()
			elif len(registered_username) == 0:
				msg.showerror("Registration Error", "Username can't be empty")
				self.create_registerPage()
			elif len(registered_password) == 0:
				msg.showerror("Registration Error", "Password can't be empty")
				self.create_registerPage()
			else:
				new_acc = {
					registered_username : {
             	     "password" : registered_password
            		}
        		}

				self.settings.users.update(new_acc)
				self.settings.save_userData(self.settings.users_path)
				self.create_menus()
				self.create_appPage()

	def exit_program(self):
		respond = msg.askyesnocancel("Exit Program", "Are you sure and really sure to close the program ?")
		if respond:
			sys.exit()
		


class GudangInfo:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	myGudangInfo = GudangInfo()
	myGudangInfo.run()