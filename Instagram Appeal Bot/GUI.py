import tkinter as tk
import subprocess
import traceback


class PythonTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Terminal")

        self.text_area = tk.Text(self.root, height=20, width=80)
        self.text_area.pack()

        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack()
        self.entry.focus_set()
        self.entry.bind('<Return>', self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.text_area.insert(tk.END, f">>> {command}\n")
        self.entry.delete(0, tk.END)

        try:
            output = subprocess.check_output(['python', '-c', command], universal_newlines=True,
                                             stderr=subprocess.STDOUT)
            self.text_area.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.text_area.insert(tk.END, e.output)

        self.text_area.see(tk.END)


# show error message "Please update OS version" if OS version is not 10.0.19041.0

traceback.print_exc()
print("Please update OS version to 10.0.19041.0")

quit()

root = tk.Tk()
terminal = PythonTerminal(root)
root.mainloop()
