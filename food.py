import requests
from bs4 import BeautifulSoup
import time
import random 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os
import json

url = "https://www.xinshipu.com/zuofa/"
count = 2241
countLimit = 100000

chrome_options = Options()
chrome_options.add_argument("disable-web-security")
#driver = webdriver.Chrome(os.path.join("./src", "chromedriver.exe"),chrome_options=chrome_options)
#driver.set_script_timeout(10) 

df = pd.read_excel("菜谱.xlsx")


def req(url):
	try:
		print("request")
		driver = webdriver.Chrome(os.path.join("./src", "chromedriver.exe"),chrome_options=chrome_options)
		driver.set_script_timeout(10) 
		driver.get(url)
		driver.implicitly_wait(10)
		print("request finish")
		return driver.page_source
	except Exception:
		driver.execute_script("window.stop()")


def save(html):
	try:
		if html != None :
			soup = BeautifulSoup(html, 'lxml')
			#print(soup.find('script', {'type': 'application/ld+json'}).get_text())
			if soup.find('script', {'type': 'application/ld+json'}) != None and html != None:
				title = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False)["name"]
				img = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False)["image"]
				ingredients = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False)["recipeIngredient"]
				cook = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False)["recipeInstructions"]
				print(url+str(count)+"  finish")
				print(str(title)+"\n"+str(ingredients)+"\n"+str(cook))
				df.loc[str(count)] =[str(title),str(img),str(ingredients),str(cook)]
				#time.sleep(2)
			#else:
				#time.sleep(3)
		if count%10==0:
			df.to_excel("菜谱.xlsx",index = False)
			print("\nsave successfully\n")
	except json.decoder.JSONDecodeError as e:
		print(url+str(count)+" jsonDecodeError")

while count < countLimit:
	count += 1
	html = req(url+str(count))
	save(html)