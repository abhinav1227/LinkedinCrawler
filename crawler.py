import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class LinkedinCrawler():
    def __init__(self, FirstName, LastName, username, password):
        self.username = username # linkedin username
        self.password = password # linkedin password
        
        #input
        self.FirstName = FirstName
        self.LastName = LastName

        # output
        self.df = pd.DataFrame(columns=["Name", "FirstName", "LastName", "Profile", "Location", "NoOfConnections", "About", "Education", "Experience"])

    def grab_website(self):
        service = Service(executable_path="chromedriver.exe")

        # Create Chromeoptions instance 
        options = webdriver.ChromeOptions() 

        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        
        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        
        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) 
        
        # Setting the driver path and requesting a page 
        driver = webdriver.Chrome(service=service, options=options) 
        
        # Changing the property of the navigator value for webdriver to undefined 
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        # with this we have the ability to grab a website
        driver.get('https://google.com')

        return driver
    
    def crawler(self):
        driver = self.grab_website()

        # its gonna take a few seconds to load the website,
        # so we will wait for the element to exist before doing any crawling

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))
        )

        linkedIn = driver.find_element(By.CLASS_NAME, "gLFyf")
        linkedIn.clear()  # clear out before adding again
        linkedIn.send_keys('linkedin' + Keys.ENTER)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'LinkedIn'))
        )

        link = driver.find_element(By.PARTIAL_LINK_TEXT, 'LinkedIn')
        link.click()
        time.sleep(5)

        # finding sign in button
        button = driver.find_element(By.XPATH, "//a[@class='nav__button-secondary btn-md btn-secondary-emphasis']")
        button.click()

        time.sleep(2)

        # logging into our linkedIn account
        driver.find_element(By.XPATH, "//input[@id='username' and @name='session_key']").send_keys(self.username)
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@id='password' and @name='session_password']").send_keys(self.password)
        time.sleep(2)

        sign_in = driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating' and @type='submit']")
        sign_in.click()
        time.sleep(5)

        # searching for input user name
        search = driver.find_element(By.XPATH, "//input[@class='search-global-typeahead__input']")
        time.sleep(3)
        search.send_keys(self.FirstName+" "+self.LastName + Keys.ENTER)
        time.sleep(5)

        # finding all the people tags
        people = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='search-results__cluster-bottom-banner artdeco-button artdeco-button--tertiary artdeco-button--muted']"))
        )
        people.find_element(By.CLASS_NAME, "app-aware-link ").click()
        time.sleep(5)
        
        for i in range(10):
            print('------',i,'-------')
            
            # going to the user profiles
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='entity-result__primary-subtitle t-14 t-black t-normal']"))
            )
            profiles = driver.find_elements(By.XPATH, "//div[@class='entity-result__primary-subtitle t-14 t-black t-normal']")
            time.sleep(10)
            profile = profiles[i].click()

            # name of the person
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']"))
                )
                name = driver.find_element(By.XPATH, f"//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text
            except NoSuchElementException:
                    name = np.nan
            #print(name)

            # profile of the person
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='text-body-medium break-words']"))
                )
                profile = driver.find_element(By.XPATH, "//div[@class='text-body-medium break-words']").text
            except NoSuchElementException:
                    profile = np.nan
            #print(profile)

            # current location of the person
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@class='text-body-small inline t-black--light break-words']"))
                )
                location = driver.find_element(By.XPATH, "//span[@class='text-body-small inline t-black--light break-words']").text
            except NoSuchElementException:
                    location = np.nan
            
            #print(location) 

            # number of connections
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@class='t-bold']"))
                )
                connections = driver.find_element(By.XPATH, "//span[@class='t-bold']").text
            except NoSuchElementException:
                    connections = np.nan

            #print(connections)

            # about section
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='display-flex ph5 pv3']/div/div/div/span"))
                )
                about = driver.find_element(By.XPATH, "//div[@class='display-flex ph5 pv3']/div/div/div/span").text
            except NoSuchElementException:
                    about = np.nan
            #print(about)

            # education
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/div/div/div/div/span"))
                )
                edu_name = driver.find_element(By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/div/div/div/div/span").text
            except NoSuchElementException:
                    edu_name = np.nan

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/span/span[@class='visually-hidden']"))
                )
                education = driver.find_element(By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/span/span[@class='visually-hidden']").text
            except NoSuchElementException:
                    education = np.nan

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/span/following-sibling::span/span[@class='pvs-entity__caption-wrapper']"))
                )
                date = driver.find_element(By.XPATH, "//div[@id='education']/following::div/following-sibling::div/ul/li/div/div/div/a/span/following-sibling::span/span[@class='pvs-entity__caption-wrapper']").text
            except NoSuchElementException:
                    date = np.nan
            #print((edu_name, education, date))

            time.sleep(10)

            # Experience

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/div/div/div/div/span"))
                )
                title = driver.find_element(By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/div/div/div/div/span").text
            except NoSuchElementException:
                    title = np.nan

            #print(title)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/span/span[@class='visually-hidden']"))
                )
                company = driver.find_element(By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/span/span[@class='visually-hidden']").text
            except NoSuchElementException:
                    company = np.nan

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/span/following-sibling::span/span[@class='pvs-entity__caption-wrapper']"))
                )
                duration = driver.find_element(By.XPATH, "//div[@id='experience']/following::div/following-sibling::div/ul/li/div/div/div/a/span/following-sibling::span/span[@class='pvs-entity__caption-wrapper']").text
            except NoSuchElementException:
                    duration = np.nan
                    
            #print((title, company, duration))

            self.df.iloc[i] = [name, name.strip().split(' ')[0], name.strip().split(' ')[1], profile, location, connections, about, (edu_name, education, date), (title, company, duration)]

            time.sleep(10)   

            # to go back to the search page and 
            driver.back()

        # will sleep for 10 sec
        time.sleep(10)
        driver.quit()

        return self.df
