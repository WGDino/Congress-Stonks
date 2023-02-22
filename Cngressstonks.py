from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from pikepdf import Pdf
from pdfminer.high_level import extract_text
import os
import pdfplumber

f = []
cols = []
x = 0
filnum = 0
filname = ""

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option('prefs', {"download.default_directory": "D:\PythonDownloads\CongressProject", "Download.prompt_for_download": False, "Download.directory_upgrade": True, "plugins.always_open_pdf_externally": True})

driver = webdriver.Chrome(options = options)
driver.get("https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure#Search")

wait = WebDriverWait(driver, 30)

last_name = "LastName"
last_name_exists = wait.until(EC.presence_of_element_located((By.ID, last_name)))
last_name_id = driver.find_element(By.ID, last_name)
last_name_id.send_keys("Pelosi")

select = Select(driver.find_element_by_id("FilingYear"))
select.select_by_visible_text("2016")

search_button = driver.find_element_by_xpath('//*[@id="search-members"]/form/div[4]/button[1]')
search_button.send_keys(Keys.RETURN)

pdfsexists = wait.until(EC.presence_of_element_located((By.ID, "DataTables_Table_0")))
pdfsexists = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tr")))

table = driver.find_element_by_id("DataTables_Table_0")
rows = table.find_elements(By.TAG_NAME, "tr")

listindex = 0

for elem in rows:
    if(x > 0):
        pdf = elem.find_elements(By.TAG_NAME, "a")
        pdf[0].send_keys(Keys.RETURN)
    x = x + 1
    
    
for col in cols:
    for y in col:
        pdfs = y.find_elements(By.PARTIAL_LINK_TEXT, "/public_disc")

sleep(5)  
driver.close()

directory = os.listdir(r"D:\PythonDownloads\CongressProject")
dirlen = len(directory)
print(dirlen)

for fil in range(0, dirlen):
    f = []
    filnum = str(filnum)
    pdfer = Pdf.open(r"D:\PythonDownloads\CongressProject\\" + directory[fil])
    pdfer.save(r"C:\Users\Chris\Downloads\easyacces.pdf")
    pdfer.close()

    sleep(1)

    with pdfplumber.open(r"C:\Users\Chris\Downloads\easyacces.pdf") as pdf:
        for page in range(0, len(pdf.pages)):
            pag = pdf.pages[page]
            f.append(pag.extract_text())
    filname = filnum
    filend = ".text"

    "".join(f)
    file1 = open(r"D:\PythonDownloads\Congresstextfiles\\" + filname + filend, "w")
    file1.writelines(f)

    filnum = int(filnum)
    filnum = filnum + 1


