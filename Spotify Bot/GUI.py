import os
import tkinter
import tkinter.messagebox
import customtkinter  # pip install customtkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from Bot import play_spotify_playlists

from tkinter import filedialog
from LoginBot import login_account

import requests
from PIL import ImageTk, Image  # pip install pillow
import webbrowser

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.app_name = "Spotify Boom"
        self.my_current_version = 1.0
        self.app_icon = tkinter.PhotoImage(file='icons/app_icon.png')
        self.app_icon = self.app_icon.subsample(2, 2)
        self.iconphoto(True, self.app_icon)

        self.title(self.app_name)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        """self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="CustomTkinter",
                                              text_font=("Roboto Medium", -16))  # font name and size in px"""

        # self.label_1.grid(row=1, column=0, pady=10, padx=10)

        # self.label_1.grid(row=1, column=0, pady=10, padx=10)
        # add image to left frame
        logo = Image.open("icons/logo.jpg")
        # image1 = logo.resize(Image.ANTIALIAS)

        # resize image to fit label

        # logo = logo.subsample(2, 2)
        instagram_icon = tkinter.PhotoImage(file='icons/instagram.png')
        instagram_icon = instagram_icon.subsample(2, 2)

        self.label_x = customtkinter.CTkLabel(master=self.frame_left,
                                              text="DAATA")

        self.label_x.grid(row=1, column=0, pady=10, padx=10)


        self.check_updates_label = customtkinter.CTkLabel(master=self.frame_left, text="CHECK FOR UPDATES:")
        self.check_updates_label.grid(row=8, column=0, pady=0, padx=20, sticky="w")

        icon = tkinter.PhotoImage(file='icons/update_icon.png')
        icon = icon.subsample(2, 2)
        # resize image to fit button

        self.update_button = customtkinter.CTkButton(master=self.frame_left,
                                                     text="UPDATES",
                                                     command=lambda: self.check_updates(self.my_current_version),
                                                     image=icon, compound="left",
                                                     corner_radius=30)
        self.update_button.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.current_version = customtkinter.CTkLabel(master=self.frame_left, text=f"version {self.my_current_version}")
        self.current_version.grid(row=10, column=0, pady=0, padx=20, sticky="w")

        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(9, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right, corner_radius=10)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ------------------> STATISTICS
        self.statistics_label = customtkinter.CTkLabel(master=self.frame_right, text=f"STATISTICS:")

        self.statistics_label.grid(row=0, column=0, pady=0, padx=20, sticky="w")
        # number of files in a folder
        number_of_files = len(os.listdir(os.getcwd() + "/Accounts FIles"))
        self.total_accounts = customtkinter.CTkLabel(master=self.frame_info, text=f"Accounts: {number_of_files}")
        self.total_accounts.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # number of proxies
        number_of_proxies = len(self.get_file_data("proxies.txt"))
        self.total_proxies = customtkinter.CTkLabel(master=self.frame_info, text=f"Proxies: {number_of_proxies}")
        self.total_proxies.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # number of playlists
        number_of_playlists = self.get_file_data("playlists.txt").__len__()
        self.total_playlists = customtkinter.CTkLabel(master=self.frame_info, text=f"Playlists: {number_of_playlists}")
        self.total_playlists.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # ------------------> Other Settings
        self.other_settings = customtkinter.CTkLabel(master=self.frame_right, text=f"Other Settings:")
        self.other_settings.grid(row=5, column=0, pady=0, padx=20, sticky="w")

        # ------------------> Buttons

        # Button 1
        add_accounts_icon = tkinter.PhotoImage(file='icons/accounts.png')
        add_accounts_icon = add_accounts_icon.subsample(2, 2)

        self.open_add_aacounts = customtkinter.CTkButton(master=self.frame_right,
                                                         text="ADD ACCOUNTS",
                                                         command=self.add_account_func,
                                                         fg_color="#FD346E",
                                                         image=add_accounts_icon, width=400)
        self.open_add_aacounts.grid(row=6, column=0, pady=20, padx=20, columnspan=4)

        # Button 2
        add_proxies_icon = tkinter.PhotoImage(file='icons/proxies.png')
        add_proxies_icon = add_proxies_icon.subsample(2, 2)

        self.open_add_proxies = customtkinter.CTkButton(master=self.frame_right,
                                                        text='ADD PROXIES',
                                                        command=self.add_proxies_func,
                                                        fg_color="#FFFF00", text_color='black',
                                                        image=add_proxies_icon, width=400)
        self.open_add_proxies.grid(row=7, column=0, pady=0, padx=20, columnspan=4, sticky="n")

        # Button 3
        add_playlists_icon = tkinter.PhotoImage(file='icons/add_playlist.png')
        add_playlists_icon = add_playlists_icon.subsample(2, 2)

        self.open_add_playlists = customtkinter.CTkButton(master=self.frame_right,
                                                          text='ADD PLAYLISTS',
                                                          command=self.add_playlists_func,
                                                          fg_color="#4AC659",
                                                          image=add_playlists_icon, width=400)
        self.open_add_playlists.grid(row=8, column=0, pady=20, padx=20, columnspan=4, sticky="n")

        # Button 4

        run_button_icon = tkinter.PhotoImage(file='icons/run bot.png')
        run_button_icon = run_button_icon.subsample(2, 2)

        self.run_button = customtkinter.CTkButton(master=self.frame_right,
                                                  text='RUN BOT',
                                                  command=self.playlist_play_func,
                                                  image=run_button_icon, width=400, height=30, corner_radius=40)
        self.run_button.grid(row=9, column=0, pady=20, padx=20, columnspan=4, sticky="n")

        # Button 5

        # Todo 1: add Logo to right frame
        # Todo 2: Add Accounts using Json file
        # Todo 3: Add Playlists with Time Frame
        # Todo 4: Add Proxies

        # configure grid layout (3x7)

    def playlist_play_func(self):
        import threading
        playlists_urls = self.get_file_data("Playlists.txt")
        print(playlists_urls)
        list_of_accounts = os.listdir(os.getcwd() + "/Accounts FIles")

        for account in list_of_accounts:
            play_spotify_playlists(account, playlists_urls)

        # for account in list_of_accounts:
        #     threading.Thread(target=play_spotify_playlists, args=(account, playlists_urls)).start()

    def check_updates(self, version):
        try:
            updates_data = requests.get('https://updates-api.shahbazshah.repl.co/updatesApi')
            updates_data = updates_data.json()
            if float(updates_data[self.app_name]['current version']) > version:
                webbrowser.open(updates_data[self.app_name]['url to download'])
            else:
                self.notification_alert("You have the latest version")
        except Exception as e:
            self.notification_alert("PLEASE CHECK YOUR NETWORK..!\n\n" + str(e))

    def get_file_data(self, file_name):
        with open(file_name) as f:
            data = f.read().strip().split('\n')
            try:
                data.remove('')
            except Exception as e:
                pass
        return data

    def add_playlists(self):
        playlist = f"{self.playlist_entry.get()}:{self.time_picker_playlist.get()}:{self.time_picker_song.get()}"

        if playlist.strip() != "":
            with open("Playlists.txt", "a") as file:
                file.write(playlist)

        if len(playlist) > 0:
            self.update_stats()
            # self.show_notification.configure(text="Proxies Added")
            self.playlist_window.destroy()

    def add_playlists_func(self):
        self.playlist_window = customtkinter.CTkToplevel(self)
        self.playlist_window.focus()
        self.playlist_window.title("Add Playlists")
        self.playlist_window.geometry("800x500")

        title_text = customtkinter.CTkLabel(master=self.playlist_window, text="ADD PLAYLISTS")
        title_text.grid(row=0, column=1, pady=20)

        # ------------------> Label
        self.playlist_entry = customtkinter.CTkEntry(master=self.playlist_window, height=30,
                                                     width=760, corner_radius=30)

        playlists = self.get_file_data("Playlists.txt")

        self.playlist_entry.focus()
        self.playlist_entry.grid(row=1, column=1, pady=20, padx=10, sticky="w")

        # time picker
        self.time_picker_playlist = customtkinter.CTkComboBox(master=self.playlist_window,
                                                              values=["Playlist Time (Minutes)", "5", "10", "15", "20",
                                                                      "25"], width=400)
        self.time_picker_playlist.grid(row=2, column=1, pady=20, padx=20, sticky="w")

        self.time_picker_song = customtkinter.CTkComboBox(master=self.playlist_window,
                                                          values=["Each Song Time (Seconds)", "1", "2", "3", "4", "5",
                                                                  "6",
                                                                  "7", "8", "9", "10", "11"], width=400)
        self.time_picker_song.grid(row=3, column=1, pady=20, padx=20, sticky="w")

        # ------------------> Buttons
        add_button = customtkinter.CTkButton(master=self.playlist_window, text="ADD Playlist",
                                             fg_color="#4AC659", command=self.add_playlists,
                                             width=100)
        add_button.grid(row=4, column=1, pady=20, padx=10)

        self.no_of_playlists = customtkinter.CTkOptionMenu(master=self.playlist_window,
                                                           values=self.get_file_data("Playlists.txt")
                                                           )
        self.no_of_playlists.grid(row=5, column=1, pady=20, padx=20, sticky="w")

        delete_button = customtkinter.CTkButton(master=self.playlist_window, text="DELETE Playlist",
                                                fg_color="red",
                                                command=lambda: self.delete_all_playlits(self.no_of_playlists.get()),
                                                width=100)
        delete_button.grid(row=6, column=1, pady=10, padx=10)

    def update_stats(self):
        number_of_proxies = len(self.get_file_data("Proxies.txt"))
        self.total_proxies.configure(text=f"Proxies: {number_of_proxies}")

        number_of_accounts = os.listdir(os.getcwd() + "/Accounts FIles")
        self.total_accounts.configure(text=f"Accounts: {len(number_of_accounts)}")

        number_of_playlists = self.get_file_data("Playlists.txt")
        self.total_playlists.configure(text=f"Playlists: {len(number_of_playlists)}")
        print("Updated")

    def add_account(self):
        spotify_email = self.email_entry.get()
        spotify_password = self.pwd_entry.get()
        self.show_account_status.configure(text="")
        if spotify_email != "" and spotify_password != "":
            try:
                login_account(spotify_email, spotify_password)
                self.accounts_window.destroy()
                self.update_stats()
            except Exception as e:
                if str(e) == 'Incorrect username or password.':
                    self.show_account_status.configure(text="Incorrect username or password..!")

    def delete_account(self):
        account_name = self.accounts_list.get()
        if str(account_name).lower() != "Select Account":
            os.remove(os.getcwd() + "/Accounts FIles/" + f"{account_name}.pkl")
            self.update_stats()
            self.accounts_window.destroy()

    def add_account_func(self):
        self.accounts_window = customtkinter.CTkToplevel(self)
        self.accounts_window.title("Add Account")
        self.accounts_window.geometry("600x400")

        title_text = customtkinter.CTkLabel(master=self.accounts_window, text="ONE TIME LOGIN")
        title_text.grid(row=0, column=1, pady=20)
        # Email
        email_label = customtkinter.CTkLabel(master=self.accounts_window, text="Email:")
        email_label.grid(row=1, column=0, pady=10, padx=0, sticky="w")
        self.email_entry = customtkinter.CTkEntry(master=self.accounts_window, width=400)
        self.email_entry.focus()
        self.email_entry.grid(row=1, column=1, pady=10, padx=0, sticky="w")

        # Password
        pwd_label = customtkinter.CTkLabel(master=self.accounts_window, text="Password:")
        pwd_label.grid(row=2, column=0, pady=10, padx=0, sticky="w")
        self.pwd_entry = customtkinter.CTkEntry(master=self.accounts_window, width=400)
        self.pwd_entry.grid(row=2, column=1, pady=10, padx=0, sticky="w")

        # Add Account Button
        add_account_button = customtkinter.CTkButton(master=self.accounts_window, text="Add Account",
                                                     command=self.add_account, width=400)
        add_account_button.grid(row=3, column=1, pady=10, padx=0)

        self.show_account_status = customtkinter.CTkLabel(master=self.accounts_window, text="")
        self.show_account_status.grid(row=4, column=1, pady=5, padx=0)

        self.delete_info_label = customtkinter.CTkLabel(master=self.accounts_window, text="DELETE ACCOUNT")
        self.delete_info_label.grid(row=5, column=1, pady=5, padx=0)

        list_of_accounts = ["Select Account"]
        list_of_accounts.extend(os.listdir(os.getcwd() + "/Accounts FIles"))
        list_of_accounts = [x.replace(".pkl", "") for x in list_of_accounts]

        self.accounts_list = customtkinter.CTkOptionMenu(master=self.accounts_window,
                                                         values=list_of_accounts
                                                         )

        self.accounts_list.grid(row=6, column=1, pady=10, padx=0)
        self.manage_accounts = customtkinter.CTkButton(master=self.accounts_window,
                                                       text="Delete Account"
                                                       , fg_color="red",
                                                       command=self.delete_account)
        self.manage_accounts.grid(row=7, column=1, pady=10, padx=0)

    def delete_all_proxies(self):
        with open("Proxies.txt", "w") as file:
            file.write("")
        self.update_stats()
        self.window.destroy()
        # self.proxies_textarea.insert(tkinter.END, "Username:Password@IP:PORT")

    def delete_all_playlits(self, pl):
        num_of_playlists = self.get_file_data("Playlists.txt")
        num_of_playlists.remove(pl)
        with open("Playlists.txt", "w") as file:
            for playlist in num_of_playlists:
                file.write(playlist + "\n")
        self.update_stats()
        self.playlist_window.destroy()

    def get_proxies(self):

        proxies = str(self.proxies_textarea.get("1.0", END)).strip()
        proxies = proxies.split("\n")
        print(f"check: {proxies}")
        proxies = [proxy for proxy in proxies if proxy != "" and proxy != "Username:Password@IP:PORT"]
        with open("Proxies.txt", "w") as file:
            file.write("")
        for proxy in proxies:
            with open("Proxies.txt", "a") as file:
                file.write(proxy + "\n")

        if len(proxies) > 0:
            self.update_stats()
            # self.show_notification.configure(text="Proxies Added")
            self.window.destroy()

    def add_proxies_func(self):
        self.window = customtkinter.CTkToplevel(self)
        self.window.title("Add Proxies")
        self.window.geometry("600x350")

        list_proxies = self.get_file_data("Proxies.txt")

        label = customtkinter.CTkLabel(master=self.window,
                                       text="ADD PROXIES")
        label.pack(pady=10)

        self.proxies_textarea = ScrolledText(master=self.window, height=10)
        for proxy in list_proxies:
            self.proxies_textarea.insert(END, proxy + "\n")
        self.proxies_textarea.focus()

        self.proxies_textarea.pack(anchor=tkinter.N, padx=10, pady=10)

        add_button = customtkinter.CTkButton(master=self.window, text="ADD", command=self.get_proxies)
        add_button.pack(pady=10)

        delete_all_proxies = customtkinter.CTkButton(master=self.window, text="DELETE ALL",
                                                     command=self.delete_all_proxies, fg_color="red")
        delete_all_proxies.pack(pady=10)

        # self.show_notification = customtkinter.CTkLabel(master=self.window, text="", text_color="red")
        # self.show_notification.pack(pady=10)

        if list_proxies == []:
            self.proxies_textarea.insert(END, "Username:Password@IP:PORT")

        # proxies_textarea.insert(0, my_proxies)

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path

        filename = filedialog.askdirectory()
        self.set_path.insert(0, filename)

    def notification_alert(self, text):
        window = customtkinter.CTkToplevel(self)
        window.title("Notification")

        window.geometry("400x200")

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text=text)
        label.pack(side="right", fill="both", expand=True, padx=40, pady=40)

    def button_event(self):
        print("Button pressed")

    def open_website(self, url):
        webbrowser.open_new(url)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
