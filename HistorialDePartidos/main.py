from selenium import webdriver
from selenium.webdriver.support.ui import Select 
import time
import pandas as pd

# Versión de Selenium = 3.141.0

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
path = 'Selenium/chromedriver'

# Obtengo la página web
driver = webdriver.Chrome(path)
driver.get(website)

# Filtro según atributos

allMatchesButton = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')
allMatchesButton.click()

dropdown = Select(driver.find_element_by_id('country'))
dropdown.select_by_visible_text('Germany')

time.sleep(5)

matches = driver.find_elements_by_tag_name('tr') 

partidos = []

for match in matches:
    partidos.append(match.text)

# Cierro la ejecucion y luego guardo la información en un dataframe
driver.quit()

df = pd.DataFrame({'partidos':partidos})
print(df)

#Guardando los datos en un archivo csv
df.to_csv ('partidos.csv',index=False)
