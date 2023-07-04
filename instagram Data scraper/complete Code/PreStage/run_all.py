import os
import pywintypes
from win10toast import ToastNotifier

# find Scaper.py files in all folders of the current directory

toast = ToastNotifier()
toast.show_toast("Scrapers", "Running all scrapers", duration=30)

os.chdir(r"C:\Users\Administrator\PycharmProjects\Scrapers\Scrapers--Anshu-\PreStage")
scraper_files = []
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith("Scraper.py"):
            if "Whittle" in str(root):
                continue
            scraper_files.append(os.path.join(root, file))

# run all scraper files
# run all scraper files
for file in scraper_files:
    file_dir = os.path.dirname(file)
    os.chdir(file_dir)



    os.system("python Scraper.py")
    print(f"Ran {file}")
# run final_checks.py

# back to original directory
original_dir = r"C:\Users\Administrator\PycharmProjects\Scrapers\Scrapers--Anshu-\PreStage"
os.chdir(original_dir)
os.system("python final_checks.py")
print("Runned")