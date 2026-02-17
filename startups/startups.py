import os
import re
import csv
import time
import startups.constants as sc
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StartUpsExtractor(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown

        # Make it faster
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        if sc.HEADLESS_MODE:
            options.add_argument('--headless') # Runs Chrome without GUI (no visible browser window) and Uses less memory and CPU
        options.add_argument('--disable-images')  # Don't load images - faster!

        super(StartUpsExtractor, self).__init__(options=options)
        # self.implicitly_wait(sc.IMPLICIT_WAIT_TIME)
        self.maximize_window()
        
    # Landing on the website
    def landing_first_page(self):
        self.get(sc.WEBSITE_URL)

    # Using context manager to close the driver
    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()

    def removing_cookie(self):
        confirm_button = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[normalize-space()="Confirm"]')
            )
        )
        confirm_button.click()

    @staticmethod
    def csv_to_excel():
        # Create a new workbook and select active sheet 
        wb = Workbook() 
        ws = wb.active 
        # Open the CSV file and read rows 
        with open(sc.CSV_OUTPUT, newline="", encoding="utf-8") as f: 
            reader = csv.reader(f) 
            for row_index, row in enumerate(reader, start=1):
                ws.append(row)
        wb.save(sc.EXCEL_OUTPUT)
        print("Excel file is created..")

    @staticmethod
    def is_valid_company_link(url: str) -> bool:
        if not url:
            return False

        url = url.strip()

        # Remove protocol if exists
        url = re.sub(r'^https?://', '', url)

        # Remove www if exists
        url = re.sub(r'^www\.', '', url)

        # Regex for domain validation
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
        )

        return bool(domain_pattern.match(url))


    def startup_inner_details(self, link:str) -> dict:

        try:
            # Navigate to the startup detail page
            self.get(link)
            
            # Wait for page to load
            WebDriverWait(self, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            data = {
                "Email": "No Info Found",
                "Company_Web": "No Info Found"
            }


            # Try to find conpany website container
            try:
                website_container = self.find_element(
                    By.CSS_SELECTOR,'div[data-block-plugin-id="field_block:node:angel_fund:field_company_website"]'
                )
                website = website_container.find_element(By.TAG_NAME, 'a').get_attribute("href")
                if self.is_valid_company_link(website):
                    data["Company_Web"] = "https://" +  website
            except Exception:
                pass

            # Try to find email container
            try:
                email_container = self.find_element(By.CSS_SELECTOR, 'div[data-block-plugin-id*="field_team_members_email"]')
                
                email = email_container.find_element(By.TAG_NAME, 'a').text
                data['Email'] = email
                    
            except Exception:
                pass

            # Extract comapny name form email 
            if data["Company_Web"] == "No Info Found" and  data["Email"] != "No Info Found":
                domain = email.split("@")[1]
                common_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
                if domain not in common_domains:
                    data['Company_Web'] = "https://" + domain
            
            return data
        
        except Exception as e:
            print(f"Error in getting the startup inner data : {e}")
        


    def collecting_page_data(self) -> list:
        try:
            # Store the current page URL before looping
            current_page_url = self.current_url
            statups_container = self.find_element(By.CLASS_NAME,"item-list")
            all_startups = statups_container.find_elements(By.TAG_NAME,"li")

            total_startups = len(all_startups)
            print(f"Total startups on this page: {total_startups}")

            startup_page_data = []

            for startup in all_startups:
                temp_dict = {}
                startup_container = startup.find_element(By.CSS_SELECTOR,'div[class="card fund team"]')
                startup_info = startup_container.find_elements(By.TAG_NAME, 'a')[1]
                startup_link = startup_info.get_attribute("href").replace("/en", "")
                startup_name = startup_info.text
                startup_page_data.append({
                    "name": startup_name,
                    "link": startup_link
                })

            return startup_page_data

        except Exception as e:
            print(f"Error occured in Collecting page data: {e}")


    def go_to_next_page(self, no_of_pages: int):
        base_url = sc.WEBSITE_URL

        for page_no in range(1, no_of_pages + 1):

            if page_no > 1:
                self.get(f"{base_url}?page={page_no}")

            WebDriverWait(self, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "item-list"))
            )

            print(f"Extracting page {page_no}")
            startup_links = self.collecting_page_data()

            # NOW process inner pages
            for idx, item in enumerate(startup_links):
                temp_dict = item.copy()
                print(f"Extracting startup number:  {idx + 1}...")
                data_dict = self.startup_inner_details(item["link"])

                if data_dict:
                    temp_dict.update(data_dict)

                    file_exists = os.path.isfile("startups.csv")
                    with open(sc.CSV_OUTPUT, "a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        
                        if not file_exists:
                            writer.writerow(["Company Name", "CityU URL", "Company Website", "Email"])
                        # writer.writerow(temp_dict)
                        writer.writerow([temp_dict["name"], temp_dict["link"], temp_dict["Company_Web"], temp_dict['Email']])
                print(f"Extracting startup number: {idx + 1} is completed!")



    
        