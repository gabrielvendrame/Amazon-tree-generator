#to avoid ssl issue
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
	ssl._create_default_https_context = ssl._create_unverified_context

import requests 
from bs4 import BeautifulSoup
import time
import datetime
import json


#Variables declaration


URL = "https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_hpc_0_353413011_2"

headers = {
	"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}




page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html5lib")

mainBox= soup.find_all("ul", id="zg_browseRoot")

dictionary= {}



for node in mainBox:
	firstList = node.find_all("a")	
	for node in firstList:		
		categoryName= ''.join(node.findAll(text=True))
		categoryLink=''.join(node.get('href'))
		dictionary[categoryName]={}
		page = requests.get(categoryLink, headers=headers)
		soup = BeautifulSoup(page.content, "html5lib")
		mainBox = soup.find_all("ul", id="zg_browseRoot")

		for node in mainBox:
			secondList = node.find_all("a")
			for node in secondList[1:]:
				subCategoryName= ''.join(node.findAll(text=True))
				dictionary[categoryName][subCategoryName]={}
				subCategoryLink= ''.join(node.get('href'))

				page = requests.get(subCategoryLink, headers=headers)
				soup = BeautifulSoup(page.content, "html5lib")
				mainBox = soup.find_all("ul", id="zg_browseRoot")

				for node in mainBox:
					thirdList = node.find_all("a")
					for node in thirdList[2:]:
						subSubCategoryName= ''.join(node.findAll(text=True))
						dictionary[categoryName][subCategoryName][subSubCategoryName]={}
						subSubCategoryLink= ''.join(node.get('href'))

						dictionary[categoryName][subCategoryName][subSubCategoryName]= "miao"
						
with open('Amazon_Tree.json', 'w') as outfile:
	json.dump(dictionary, outfile)
	print(datetime.datetime.now(), "JSON Aggiunto")				
