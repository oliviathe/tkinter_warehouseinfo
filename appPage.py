import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk
from datetime import datetime
from time import time

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_data = self.settings.database[0]
		self.last_current_data_index = 0
		self.update_mode = False
		self.database_index = []

		super().__init__(parent) #parent = window.container
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_and_right_frame()		

	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")

		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")

		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_and_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h)
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio), int(2*i_h/ratio/3)) # (x,y)
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.search_box_frame = tk.Frame(self.left_frame, bg="white", width=frame_w, height=frame_h//4)
		self.search_box_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.search_box_frame, bg="white", fg="black", font=("Arial", 12), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.search_box_frame, bg="white", fg="black", text="Find", font=("Arial", 12), command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.search_box_frame.grid_columnconfigure(0, weight=3)
		self.search_box_frame.grid_columnconfigure(1, weight=1)

	def show_list_database_in_listbox(self):
		database = self.settings.database
		# for data in database:
		# 	for productid, info in data.items():
		# 		fulitemmerk = f"{info['itemname']} {info['itemmerk']}"
		# 		self.database_list_box.insert("end", fulitemmerk)
		for index in self.database_index:
			data = database[index]
			for productid, info in data.items():
				fulitemmerk = f"{info['itemname']} {info['itemmerk']}"
				self.database_list_box.insert("end", fulitemmerk)

	def show_all_data_in_listbox(self):
		self.database_list_box.delete(0, 'end')
		database = self.settings.database
		self.database_index = []
		counter = 0
		for data in database:
			self.database_index.append(counter)
			counter += 1
		self.show_list_database_in_listbox()

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5
		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.database_list_box = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.database_list_box.pack(side="left", fill="both", expand=True)

		self.database_scroll = tk.Scrollbar(self.left_content)
		self.database_scroll.pack(side="right", fill="y")

		self.show_all_data_in_listbox()

		self.database_list_box.configure(yscrollcommand=self.database_scroll.set) # set di Scroll
		self.database_scroll.configure(command=self.database_list_box.yview) # yview di Listbox

		self.database_list_box.bind("<<ListboxSelect>>", self.clicked_item_inListBox)


	def clicked_item_inListBox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try :
				clicked_item_index = selection[0]
			except IndexError:
				clicked_item_index = self.last_current_data_index
			index = self.database_index[clicked_item_index]
			self.last_current_data_index = index
			self.current_data = self.settings.database[index]
			print(clicked_item_index,"=>",index)
			for ProductID, info in self.current_data.items():
				productid = ProductID
				fulitemmerk = info['itemname']+" "+info['itemmerk']
				stok = info['stok']
				supplier = info['supplier']
				lastchanged = info['lastchanged']

			self.fulitemmerk_label.configure(text=fulitemmerk)
			self.table_info[0][1].configure(text=productid)
			self.table_info[1][1].configure(text=stok)
			self.table_info[2][1].configure(text=supplier)
			self.table_info[3][1].configure(text=lastchanged)


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="bisque")
		self.right_header.pack()
		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data_dictionary = list(self.current_data.values())[0]
		fulitemmerk = f"{data_dictionary['itemname']} {data_dictionary['itemmerk']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.fulitemmerk_label = tk.Label(self.detail_header, text=fulitemmerk, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
		self.fulitemmerk_label.pack()

		self.right_header.grid_rowconfigure(0, weight=1)
		self.right_header.grid_columnconfigure(0, weight=1)


	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True, pady=90)
		self.create_detail_right_content()

	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for ProductID, info in self.current_data.items():
			info = [
				['Product ID :', ProductID],
				['Stock :', info['stok']],
				['Supplier :', info['supplier']],
				['Last Changed :', info['lastchanged']]
			]
		self.table_info = []
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)


	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack(expand=True)

		self.create_detail_right_footer()


	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)

	def recreate_right_frame(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()


	def recreate_right_frame_after_delete(self):

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def recreate_right_frame_after_add_new(self):
		self.detail_add_new_header.destroy()
		self.detail_add_new_content.destroy()
		self.detail_add_new_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for ProductID, info in self.current_data.items():
			info = [
				['Product Name :', info['itemname']],
				['Product Merk :', info['itemmerk']],
				['Stock :', info['stok']],
				['Supplier :', info['supplier']]
			]
		self.table_info = []
		self.entry_update_data_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					aRow.append(label)
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_update_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_data_vars[row])
					entry.insert(0, info[row][column])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)

		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_data_btn, self.clicked_cancel_data_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)


	def clicked_delete_btn(self):
		self.update_mode = True
		#print(self.last_current_data_index)

		confirm = msg.askyesnocancel('Item Delete Confirmation', 'Are you sure you want to delete this item ?')
		index  = self.last_current_data_index
		if confirm:
			self.settings.database.pop(index)
			self.settings.save_data_to_json()
			self.last_current_data_index = 0
			self.current_data = self.settings.database[self.last_current_data_index]

			self.recreate_right_frame_after_delete()
			self.show_all_data_in_listbox()

		self.update_mode = False

	def clicked_add_new_btn(self):
		self.update_mode = True

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_add_new_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="green")
		self.detail_add_new_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.add_new_label = tk.Label(self.detail_add_new_header, text="Add New Product", font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound='c', bg="white")
		self.add_new_label.pack()

		self.right_header.grid_rowconfigure(0, weight=1)
		self.right_header.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4

		self.detail_add_new_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_content.grid(row=0, column=0, sticky="nsew")

		info = [
			['Product Name :', None],
			['Product Merk :', None],
			['Product ID :', None],
			['Stock :', None],
			['Supplier :', None]
		]
		self.table_info = []
		self.entry_update_data_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
		rows, columns = len(info), len(info[0]) # 3, 2
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_add_new_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					aRow.append(label)
					label.grid(row=row, column=column, sticky=sticky)
				else:
					entry = tk.Entry(self.detail_add_new_content, font=("Arial", 12), bg="white", textvariable=self.entry_update_data_vars[row])
					sticky = "w"
					aRow.append(entry)
					entry.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		self.right_content.grid_rowconfigure(0, weight=1)
		self.right_content.grid_columnconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_add_new_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_add_new_data_btn, self.clicked_cancel_add_new_data_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_add_new_footer, text=feature, bg="white", fg="black", bd=0, font=("Arial", 12, "bold"), command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20)
			self.buttons_features.append(button)

		self.right_footer.grid_rowconfigure(0, weight=1)
		self.right_footer.grid_columnconfigure(0, weight=1)


	def clicked_save_data_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('Save Confirmation', 'Are you sure to update this item ?')
		
		index = self.last_current_data_index
		self.current_data = self.settings.database[index]
		for ProductID, info in self.current_data.items():
			frozenset(info)
			productid = ProductID
		if confirm:
			itemname = self.entry_update_data_vars[0].get()
			itemmerk = self.entry_update_data_vars[1].get()
			#productid = self.entry_update_data_vars[2].get()
			stok = self.entry_update_data_vars[2].get()
			supplier = self.entry_update_data_vars[3].get()
			self.settings.database[index] = {
				productid : {
					"itemname" : itemname,
					"itemmerk" :itemmerk,
					"stok" : stok,
					"supplier" : supplier,
					"lastchanged" : datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
				}
			}
			self.settings.save_data_to_json()
		self.current_data = self.settings.database[index]

		self.recreate_right_frame()

		self.database_list_box.delete(0, 'end')
		self.show_list_database_in_listbox()


	def clicked_cancel_data_btn(self):
		self.update_mode = False

		self.recreate_right_frame()


	def clicked_search_btn(self):

		item_search = self.entry_search_var.get()
		if item_search:
			item_search1 = item_search.capitalize()
			database = self.settings.database
			self.database_index = []
			index_counter = 0
			for data in database:
				for ProductID, info in data.items():
					if item_search in ProductID:
						print(ProductID)
						self.database_index.append(index_counter)
					elif item_search in info['itemname']:
						print(info['itemname'])
						self.database_index.append(index_counter)
					elif item_search1 in info['itemname']:
						print(info['itemname'])
						self.database_index.append(index_counter)
					elif item_search in info['itemmerk']:
						print(info['itemmerk'])
						self.database_index.append(index_counter)
					elif item_search in info['itemmerk']:
						print(info['itemmerk'])
						self.database_index.append(index_counter)
				index_counter += 1
			print(self.database_index)
			self.database_list_box.delete(0, 'end')
			self.show_list_database_in_listbox()
		else:
			self.show_all_data_in_listbox()


	def clicked_save_add_new_data_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('Save Confirmation', 'Are you sure you want to add this item ?')
		
		if confirm:
			itemname = self.entry_update_data_vars[0].get()
			itemmerk = self.entry_update_data_vars[1].get()
			stok = self.entry_update_data_vars[2].get()
			supplier = self.entry_update_data_vars[3].get()

			addnewdata_timer = datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
			self.database = self.settings.load_data_from_json()
			self.settings.data_counter+=1
			current_productid = str(self.settings.data_counter)+str(datetime.now().strftime("%H%d%m%Y"))

			new_data = {
				current_productid : {
					"itemname" : itemname,
					"itemmerk" :itemmerk,
					"stok" : stok,
					"supplier" : supplier,
					"lastchanged" : addnewdata_timer
				}
			}
			self.settings.database.append(new_data)
			self.settings.save_data_to_json()
			self.settings.save_data_counter()
		index = len(self.settings.database)-1
		self.last_current_data_index = index
		self.current_data = self.settings.database[self.last_current_data_index]

		self.recreate_right_frame_after_add_new()

		self.database_list_box.delete(0, 'end')
		self.show_all_data_in_listbox()



	def clicked_cancel_add_new_data_btn(self):
		pass
