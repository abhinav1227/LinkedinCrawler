## LinkedinCrawler
In this task, given a name, we are scraping the first 10 profiles that we get with the given name.

* For the API script(linedinAPICrawler.ipynb):
     - I was able to do a basic call.
     - Because till now, LinkedIn hasn't authenticated 'r_liteprofile' in the app I created in the LinkedIn developer portal, I couldn't implement it to the full extent.

* For the Basic Crawler(linkedinCrawler.py)
     - We started by grabbing a website using Selenium (https://google.com).
     - We crawled to LinkedIn, logged in, and searched the Input name.
     - Using XPATH and Selenium scraped the most important data of the user.

