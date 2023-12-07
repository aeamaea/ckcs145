from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Expect

# set up options for webdriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# create instance of webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = 'https://www.google.com'
driver.get(url)

# we find the search bar using it's name attribute value
searchBar = driver.find_element(By.NAME, 'q')

# set keyword or search criteria
keyword = 'hyper cars' 

# first we send our keyword to the search bar followed by the enter
searchBar.send_keys(keyword)
searchBar.send_keys('\n')

def scrape():
   pageInfo = []
   try:
      # wait 10 sexpectonds for search results to be retrieved
      WebDriverWait(driver, 10).until(
      Expect.presence_of_element_located((By.CLASS_NAME, "g"))
      )
    
   except Exception as e:
      print(e)
      driver.quit()
      
   # process the search results
   searchResults = driver.find_elements(By.CLASS_NAME, 'g')
   for result in searchResults:
       element = result.find_element(By.CSS_SELECTOR, 'a')
       link = element.get_attribute('href')
       
       # Append harvested data to pageInfo
       pageInfo.append({
           'element' : element.text, 
           'result' : result.text,
           'hyperlink' : link
       })
       
       # For debugging purposes in order to see that loop is running
       print('result', result.text)
       print('element: ', element.text)
       print('hyperlink: ', link)
       
   return pageInfo


# Number of pages to harvest
numPages = 5
# Storage for harvested data
infoAll = []

# Begin harvesting search results.  We are harvesting a total of 5 pages.

# Harvested data from first page
infoAll.extend(scrape())

# Harvested data from subsequent pages
try:
   for i in range(0 , numPages - 1):
      # Click on next link form the search results page
      nextButton = driver.find_element(By.LINK_TEXT, 'Next')
      nextButton.click()
      
      # Harvest next search results page
      infoAll.extend(scrape())
except:
   print("ERROR while trying to click Next. Stopping!")

# Print all harvested data
print()
print('======[ Harvested Data From Search ]======')
print(infoAll)
