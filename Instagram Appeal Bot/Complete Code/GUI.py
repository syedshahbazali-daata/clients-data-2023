import ctypes

def set_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# Example usage
new_title = "My New CMD Title"
set_cmd_title(new_title)

input("add: ")

