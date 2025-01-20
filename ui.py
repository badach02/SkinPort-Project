import json
from tkinter import *
from pull_data import pull_items, pull_sales, pull_transaction_history
from write_sheet import find_skin_data, fix_data, write_skin

with open("json/watch_list.json", "rb") as file:
    skins = json.load(file)
    file.close()


is_running = False


def write_json(app):
    global file
    global skins

    entry = app.add_text.get()
    skins.append(entry)
    skins_json = json.dumps(skins, indent=2)

    with open("json/watch_list.json", "w") as file:
        file.write(skins_json)
        file.close()

    app.list_box.insert(END, entry)


def remove_skin(app):
    global file
    global skins

    entry = app.remove_text.get()
    skins.remove(entry)
    skins_json = json.dumps(skins, indent=2)

    with open("json/watch_list.json", "w") as file:
        file.write(skins_json)
        file.close()

    for index in range(app.list_box.size()):
        if app.list_box.get(index) == entry:
            app.list_box.delete(index)


def execute(app, clicked):
    global is_running
    global skins

    if clicked and is_running:
        is_running = False
        app.status_label.config(text="Status: Stopped")
        app.exec_button.config(text="Execute Program", bg="Green")
    else:
        is_running = True
        use_live_data = True

        app.status_label.config(text="Status: Running")
        app.exec_button.config(text="Stop", bg="Red")

        with open("json/watch_list.json", "rb") as exec_file:
            skins = json.load(exec_file)
            exec_file.close()

        if use_live_data:
            itemData = pull_items(use_live_data)
            salesData = pull_sales(use_live_data)
            ##transactionData = pull_transaction_history(use_live_data)
        elif not use_live_data:
            print("use_live_data is false")
            with open("json/items.json", "rb") as exec_file:
                itemData = json.load(exec_file)
            with open("json/sales.json", "rb") as exec_file:
                salesData = json.load(exec_file)
            ##with open("json/transactions.json", "rb") as exec_file:
                ##transactionData = json.load(exec_file)
            exec_file.close()

        skinData = find_skin_data(skins, itemData, salesData)
        passData = fix_data(skinData)

        print("Starting to write data to google sheets...")
        write_skin(passData, 1, 4, use_live_data)
        print("Finished writing data to google sheets...")

        app.window.after(240000, execute, app, False)


class application:
    def __init__(self, window):
        self.window = window
        window.geometry("750x500")
        window.iconbitmap("media/ak.ico")
        window.title("CS Skins")

        self.header_label = Label(window, text="Items in watch_list.json:")
        self.header_label.place(relx=0, rely=0, anchor=NW)

        self.status_label = Label(window, text="Status: Stopped")
        self.status_label.place(relx=0.45, rely=0.98, anchor=SE)

        self.add_button = Button(window, text="Add an item to watch_list.json", command=lambda: write_json(self))
        self.add_button.place(relx=0.35, rely=0.2, anchor=NW)

        self.add_text = Entry(window, width=50)
        self.add_text.place(relx=0.35, rely=0.27, anchor=NW)

        self.remove_button = Button(window, text="Remove an item from watch_list.json", command=lambda: remove_skin(self))
        self.remove_button.place(relx=0.35, rely=0.4, anchor=NW)

        self.remove_text = Entry(window, width=50)
        self.remove_text.place(relx=0.35, rely=0.47, anchor=NW)

        self.list_box = Listbox(window, height=30, width=40)
        self.list_box.place(relx=0, rely=0.04, anchor=NW)

        self.exec_button = Button(window, text="Execute Program", command=lambda: execute(self, True), bg="Green")
        self.exec_button.place(relx=.98, rely=.98, anchor=SE)

        for skin in skins:
            self.list_box.insert(END, skin)


