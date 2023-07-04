a = "Tel.: (905) 671-4674                                              Toll Free: (800) 595-9395"
########################################################################################################################
# Functions
import csv
def check_libraries_exist(libraries: list):
    import importlib
    for library in libraries:
        try:
            importlib.import_module(library)

        except:
            print(f"ERROR: {library} is not installed. Please install it and try again.")
            # install library
            import subprocess
            subprocess.check_call(["python", '-m', 'pip', 'install', library])

            exit()


check_libraries_exist(["undetected_chromedriver"])
import time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def get_file_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')
    return data


def find_element_send_text(ele, text, clear=True):
    while True:
        try:
            input_field = driver.find_element(By.XPATH, ele)
            if clear:
                input_field.clear()
            input_field.send_keys(text)

            break
        except:
            time.sleep(0.1)


def specific_clicker(ele):
    while True:
        try:
            element = driver.find_element(By.XPATH, ele)
            webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

            break
        except Exception as e:
            # print(e)
            pass


def specific_clicker2(ele):
    try:
        element = driver.find_element(By.XPATH, ele)
        webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()

    except Exception as e:
        # print(e)
        pass


def get_text(ele):
    while True:
        try:
            element = driver.find_elements(By.XPATH, ele)
            texts = [str(x.text) for x in element]
            return texts
        except Exception as e:
            # print(e)
            pass


def get_text_pass(ele):
    try:
        element_text = driver.find_element(By.XPATH, ele).text


    except Exception as e:
        element_text = "N/A"
    return element_text


def get_year_data(year_no):
    try:
        x = str(driver.find_elements(By.XPATH, f"//*[text()='{year_no}']/ancestor::tr")[-1].text).split(" ")[-1]
    except:
        x = "N/A"
    return x


def close_chrome():
    import os
    try:
        os.system("taskkill /im chrome.exe /f")
    except:
        pass


options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.maximize_window()
urls = ['https://www.aerialevolution.ca/member-directory/#!biz/id/6387dcb87dbc334b193b1a9d',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565e521137215f3a9031',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565a521137215f3a8fd4',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565e521137215f3a9021',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fdc',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6346c7b68ebf656439101b2b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/63474dbe1b3ced07f14697cc',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/622f7dc2293f4f649a757613',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/642cbf6cf353df2aa1232663',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/60f5e3ff924f2a0d2c79beba',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62a38b0f881eeb03804b492b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62e9baafc5068f5168081245',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6389180718053510d603d6c5',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/620bf44bf42850657878edea',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/628f8caee0873653481b472c',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/613a337bc719813788405d26',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565c521137215f3a8ff0',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62a3bf6cc6413708be4c29ba',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565d521137215f3a9008',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6323ccf34b55f6776e6f0eb2',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/622bd31ca8aca21b6a7a6b8f',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565e521137215f3a902b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565c521137215f3a8ff3',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565a521137215f3a8fd5',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/61927eda8bd27a6b1642000f',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fec',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/635ab651621c6c1a22635652',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/631ed479765bf1440e1e13b3',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/638cc299f37c18009c6a229e',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fe4',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fde',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6309179158d4de5e80581ea1',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/627d7c4f21f6f714eb7f8fd6',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/632a41e22de0ea67da3b4d4f',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/63ade7bfac78b641f17daccb',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/618d98b70e466f20d46700a8',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/63d2fc2795cce04d76692bd2',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/63f5131aaa600c05892af8ab',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565e521137215f3a9037',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6384becc850b607a4461d209',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565c521137215f3a8ffa',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/632231e4e2cedb243430ac92',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62f13c4ce379356114292932',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62fff519df6d9d79ee312a7e',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62c45b4ec6873c53a16e1be2',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6330c618413c2a50a03c7294',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565d521137215f3a9010',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/618bfbf7cc3a9a132067f375',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6333067a4b2a5f0d190e800b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fea',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/60ff49d186ce7314cf498c62',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/633dc726d0d3d608f04a52bb',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62e9411b2812fe03ce170962',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6387f4ff46b70a429d37ccb3',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/615d975e8e061d54ce210ca5',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565d521137215f3a9011',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6387fc1ac44d562573584163',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/64432260e9e4e5649359fb5c',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/625dcc765362df07956c4c67',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/64381700944d1406227695f1',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565b521137215f3a8fe0',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/635314bb23c45060407cf8a4',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/606cafe17dcf5c5c0c53b2db',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/62fcfe7d784d046c7b428262',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6377b653cb5ba527cb49e474',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/631f7d5061d2dd1a35174132',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/61a0053b353a1a15eb0b7540',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/609fe22955f5b638d37bfdd9',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/63880e8a0b4dbe072d066eb9',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/638806bb798df574663c9c34',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/61dcd74e428ea3459d2b826c',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/609fe22c55f5b638d37bfe28',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/609fe22955f5b638d37bfdcf',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/609fe22b55f5b638d37bfe03',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/609fe22c55f5b638d37bfe32',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/60a3e2a80390444a79530a3b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/614ab35fa6e4e552e65c27cb',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/6352e66252ded177c3569f8b',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/636c46a21473b161637b3e29',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/619405806f42241bed770305',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/605a565d521137215f3a900e',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/636c052c603adc602e7e4b93',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/60b9284518289d0ded0d7e4d',
        'https://www.aerialevolution.ca/member-directory/#!biz/id/643839742ee8a05463048a2a']
for single_url in urls:
    uid = single_url.split('/')[-1]
    driver.get(single_url)
    time.sleep(1)

    for check in range(10):
        try:
            driver.find_element(By.XPATH, '//div/h1/text()')
            # scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            break
        except:
            time.sleep(0.1)
    xpath = f'//div[@id="SFbizctc{uid}"]'
    print(xpath)

    title = get_text_pass(f'{xpath}//h3')
    phone = get_text_pass(f'{xpath}//a[@title="Call"]')
    website = get_text_pass(f'{xpath}//a[@title="Website"]')
    descriptions = [str(i.text) for i in driver.find_elements(By.XPATH, f'//div[@class="SFbizbox"]/p')]
    description = " ".join(descriptions)
    email = get_text_pass(f'{xpath}//a[@title="Email"]')

    source = "https://www.aerialevolution.ca/member-directory/"

    # Title	Email	Phone 	Website	Category	Description	Source	Extra
    record = [title, email, phone, website, f"{uid}", description, source, "NA"]
    with open('aerialevolution.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(record)
    print(record)

