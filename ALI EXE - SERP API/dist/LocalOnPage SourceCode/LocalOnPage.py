import os
import tkinter
import tkinter.messagebox
from datetime import datetime
from urllib.parse import urlparse
import customtkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from databaseFunctions import get_column_data, update_sheet, cell_update
from GetData import serp_result_finder
import webbrowser
from multiprocessing import freeze_support
freeze_support()

# colors
theme_color = "#F5F4F4"
primary_color = "#ffae33"
secondary_color = "#ECE7E5"
tertiary_color = "#12100c"
other_text_color = "#8e8c8b"

# Fonts
font_family = "Roboto"

"""
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"""


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 540

    def __init__(self):
        super().__init__()

        self.app_name = "Local OnPage"
        self.my_current_version = 1.0
        self.app_icon = tkinter.PhotoImage(file='icons/app_icon.png')
        # at top of the window

        # ------------------------------------------------------------
        try:
            with open("Database/License Key.txt", "r") as f:
                self.my_license_key = f.read().strip()
                print(self.my_license_key)


            # index_of_license_key = self.license_keys.index(self.my_license_key)


            self.name_customer = "test"
            self.business = "test"
            self.package = "LifeTime"
            self.start_date = "12-12-2020"
            self.end_date = "12-12-2040"

            # convert string to datetime object

            self.days_left = "Unlimited"
            self.searches_left = "Unlimited"
            self.api_key = self.my_license_key

            print([self.name_customer, self.business, self.package, self.start_date, self.end_date, self.days_left,
                   self.searches_left])
        except Exception as e:
            print(e)
            self.license_keys = list(get_column_data(0, 1))
            self.start_date = "Not Found"
            self.end_date = "Not Found"
            self.days_left = "Not Found"
            self.searches_left = "Not Found"
            self.name_customer = "Not Found"
            self.business = "Not Found"
            self.package = "Not Found"
            self.api_key = "Not Found"

        # ------------------------------------------------------------
        self.app_icon = self.app_icon.subsample(2, 2)
        self.iconphoto(True, self.app_icon)

        self.title(self.app_name)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.configure(background='#F5F4F4')
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self, fg_color=theme_color)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        key_icon = tkinter.PhotoImage(file='icons/key.png')
        key_icon = key_icon.subsample(2, 2)

        if "License Key.txt" not in os.listdir("Database"):

            self.activation_button = customtkinter.CTkButton(master=self.frame_left,
                                                             text="ADD SERP API KEY",
                                                             command=self.license_key_window,
                                                             fg_color='#f7e200', text_color='black', border_width=1,
                                                             image=key_icon)

            self.activation_button.grid(row=4, column=0, pady=10, padx=20)
        else:
            self.activation_button = customtkinter.CTkButton(master=self.frame_left,
                                                             text="ACTIVATED",
                                                             fg_color='#00f73f', text_color='white', border_width=1,
                                                             state='disabled', image=key_icon)

            self.activation_button.grid(row=4, column=0, pady=10, padx=20)

        # self.check_updates_label = customtkinter.CTkLabel(master=self.frame_left, text="SEND FEEDBACK TO US:")
        # self.check_updates_label.grid(row=8, column=0, pady=0, padx=20, sticky="w")
        #
        # icon = tkinter.PhotoImage(file='icons/feedback.png')
        # # resize image to fit button
        # icon = icon.subsample(2, 2)
        #
        # self.feedback_button = customtkinter.CTkButton(master=self.frame_left,
        #                                                text="FEEDBACK",
        #                                                command=self.feedback_window_page,
        #                                                image=icon, compound="left",
        #                                                fg_color='#12100c', text_color='white',
        #                                                corner_radius=30)
        # self.feedback_button.grid(row=9, column=0, pady=10, padx=20, sticky="w")
        #
        # self.current_version = customtkinter.CTkLabel(master=self.frame_left, text=f"Till {self.end_date}")
        # self.current_version.grid(row=10, column=0, pady=0, padx=20, sticky="w")

        # ============ frame_right ============
        # configure grid layout (3x7)

        # ------------------> STATISTICS
        self.statistics_label = customtkinter.CTkLabel(master=self.frame_right, text=f"STATISTICS:")
        self.statistics_label.grid(row=0, column=0, pady=0, padx=20, sticky="w")

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right, corner_radius=10, fg_color=primary_color)
        self.frame_info.grid(row=1, column=0, pady=10, padx=20, rowspan=2)

        self.total_accounts = customtkinter.CTkLabel(master=self.frame_info, text=f"SEARCH LEFT: {self.searches_left}")
        self.total_accounts.grid(row=0, column=0, pady=20, padx=13, sticky="w")

        # number of proxies

        self.package_name = customtkinter.CTkLabel(master=self.frame_info, text=f"PACKAGE: {str(self.package).upper()}")
        self.package_name.grid(row=0, column=1, pady=20, padx=13, sticky="w")

        # number of playlists

        self.days_left_show = customtkinter.CTkLabel(master=self.frame_info, text=f"DAYS LEFT: {self.days_left}"
                                                     )
        self.days_left_show.grid(row=0, column=2, pady=20, padx=13, sticky="w")

        # ------------------> Details

        row_number = 5
        # Email
        my_url = customtkinter.CTkLabel(master=self.frame_right, text="ENTER URL:",  anchor="w")
        my_url.grid(row=row_number, column=0, pady=10, padx=20, sticky="w")
        self.url_entry = customtkinter.CTkEntry(master=self.frame_right, width=500)
        self.url_entry.focus()
        self.url_entry.grid(row=row_number + 1, column=0, pady=0, padx=20, sticky="w")

        # set locationskdmds
        set_location = customtkinter.CTkLabel(master=self.frame_right, text="SET LOCATION:",
                                              anchor="w")
        set_location.grid(row=row_number + 2, column=0, pady=10, padx=20, sticky="w")
        self.set_location_entry = customtkinter.CTkEntry(master=self.frame_right, width=500)

        self.set_location_entry.grid(row=row_number + 3, column=0, pady=0, padx=20, sticky="w")

        # keywords
        set_keywords = customtkinter.CTkLabel(master=self.frame_right, text="SET KEYWORDS:",
                                              anchor="w")
        set_keywords.grid(row=row_number + 4, column=0, pady=10, padx=20, sticky="w")
        self.set_keywords_entry = customtkinter.CTkEntry(master=self.frame_right, width=500)

        self.set_keywords_entry.grid(row=row_number + 5, column=0, pady=0, padx=20, sticky="w")

        # words
        set_words = customtkinter.CTkLabel(master=self.frame_right, text="SET WORDS:",
                                           anchor="w")
        set_words.grid(row=row_number + 6, column=0, pady=10, padx=20, sticky="w")
        self.set_words_entry = customtkinter.CTkEntry(master=self.frame_right, width=500)
        self.set_words_entry.grid(row=row_number + 7, column=0, pady=0, padx=20, sticky="w")

        # Search it
        self.search_it = customtkinter.CTkButton(master=self.frame_right, text="SEARCH NOW",
                                                 fg_color=primary_color, text_color=tertiary_color, corner_radius=30,
                                                 height=40,
                                                 command=self.get_results)
        self.search_it.grid(row=row_number + 8, column=0, pady=20, padx=20, sticky="e")

    def get_results(self):
        x  = 0
        if x==0:
            import threading
            url = str(self.url_entry.get()).strip()
            location = str(self.set_location_entry.get()).strip()
            keywords = str(self.set_keywords_entry.get()).strip()
            words = str(self.set_words_entry.get()).strip()

            domain = urlparse(url).netloc
            filename = f"{domain}.csv"

            if url == "" or location == "" or keywords == "" or words == "":
                messagebox.showerror("ERROR", "Please fill all the fields")
            else:
                self.search_it.configure(text="SCRAPING...", state="disabled")
                threading.Thread(target=serp_result_finder,
                                 args=(keywords, location, str(self.api_key).strip(), words, filename)).start()

                # cell_update(0, self.customer_index + 1, 7, f"{int(self.searches_left) - 1}")
                # self.total_accounts.configure(text=f"SEARCH LEFT: {int(self.searches_left) - 1}")
                # self.search_it.configure(text="SEARCH NOW", state="normal")



        elif int(self.days_left) <= 0:
            messagebox.showerror("ERROR", "Your package has expired")
        elif int(self.searches_left) <= 0:
            messagebox.showerror("ERROR", "You have no searches left")

    def feedback_submit_func(self):
        text = str(self.feedback_entry.get("1.0", END)).strip()
        current_date = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        if len(text) > 5:
            try:
                update_sheet(1,
                             [self.name_customer, self.business, self.package, self.end_date, self.my_license_key, text,
                              str(current_date)])
                self.feedback_window.destroy()
            except:
                pass

    def feedback_window_page(self):
        print("checked")
        self.feedback_window = customtkinter.CTkToplevel(self)
        self.feedback_window.title("FEEDBACK PAGE")
        self.feedback_window.geometry("550x420")

        label = customtkinter.CTkLabel(master=self.feedback_window,
                                       text="ENTER FEEDBACK OR ERROR",

                                       height=40, width=600, )

        label.pack(pady=10)

        self.feedback_entry = ScrolledText(master=self.feedback_window, height=10, width=50)
        self.feedback_entry.focus()
        self.feedback_entry.pack(pady=50)

        self.feedbac_submit_button = customtkinter.CTkButton(master=self.feedback_window, text="SUBMIT",
                                                             fg_color=primary_color, text_color=tertiary_color,
                                                             corner_radius=30,
                                                             height=40,
                                                             command=self.feedback_submit_func
                                                             )
        self.feedbac_submit_button.pack(pady=10)

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

    def activate_license_key_func(self):
        license_key_entered = str(self.license_entry.get()).strip()

        if len(license_key_entered) > 5:
            print(license_key_entered)


            with open("Database/License Key.txt", "w") as f:
                    f.write(license_key_entered)
            self.license_window.destroy()

            # close the app
            self.destroy()



    def license_key_window(self):
        self.license_window = customtkinter.CTkToplevel(self)
        self.license_window.title("ACTIVATION")
        self.license_window.geometry("600x350")

        label = customtkinter.CTkLabel(master=self.license_window,
                                       text="ENTER SERP API KEY",
                                       )

        label.pack(pady=10)

        self.license_entry = customtkinter.CTkEntry(master=self.license_window, width=500)
        self.license_entry.focus()
        self.license_entry.pack(pady=50)

        self.submit_button = customtkinter.CTkButton(master=self.license_window, text="SUBMIT",
                                                     fg_color=primary_color, text_color=tertiary_color,
                                                     corner_radius=30,
                                                     height=40,
                                                     command=self.activate_license_key_func)
        self.submit_button.pack(pady=10)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()


# Pyinstaller LocalOnPage.py --onefile --add-data "C:/Users/shahb/AppData/Local/Programs/Python/Python311/Lib/site-packages/customtkinter;customtkinter/" --icon="C:\Users\shahb\PycharmProjects\ClientsData\ALI EXE - SERP API\icons\app_icon.ico"
