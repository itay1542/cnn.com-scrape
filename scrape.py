#!usr/bin/env

from bs4 import BeautifulSoup

from selenium import webdriver 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import re

CNN = 'https://edition.cnn.com/'
webdriver=webdriver.Chrome('/usr/bin/chromedriver') 


class GetData:


	def __init__(self,url):

		self.url = url


	def scrape(self):	

		try:
			print("scraping www.cnn.com , please wait as it might take a while :)")	

			webdriver.get('https://edition.cnn.com/')
			element = WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cn__title ")))	
			source = webdriver.page_source
			soup = BeautifulSoup(source,'html.parser')

			article_links = []
			for ul in soup.find_all('ul'):
				if(ul.h2 and 'Top' in ul.h2.string): #if the ul element has a h2 child, and Top is in the h2 string
					for li in ul.find_all('li'):
						article_links.append(li.find('a').get('href'))
			
			self.scrape_from_articles(article_links)

		except TimeoutException as exception:
			print('timed out, check internet connection and try again')

		finally:
			print('done')
			webdriver.close()
			return ''	

				
	def scrape_from_articles(self,links):

		try:

			articles_array = []
			for link in links:
				webdriver.get('https://edition.cnn.com'+link)
				x = WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
				source = webdriver.page_source
				soup = BeautifulSoup(source,'html.parser')

				title = soup.h1.string
				paragraph = ''
				img_links = []

				for p in soup.find_all('p'):
					if(p.cite):
						paragraph=p.get_text()

				for img in soup.find_all('img'):		
						if("media__image" in str(img.get('class')) and not re.match('data:(.*)',img.get('src'))):
							img_links.append(img.get('src'))				
				article = {
					"title" : title,
					"paragraph" : paragraph,
					"links" : img_links
					}
				articles_array.append(article)
		
		except TimeoutException as exception:
			print('timed out, check internet connection and try again')

		finally:
			self.print_to_screen(articles_array)
			return 	


	def print_to_screen(self,array):

		print("\nTop Articles: \n")
		
		for article in array:
			images=""
			for link in article['links']:
				images += link[2:] + "\n"
					
			print('\033[1m' + #bold text
				article['title'] 
				+ "\033[0m \n" #end bold text
				+ article['paragraph'] 
				+ " \nimages: \n" 
				+ images 
				+ "\n \n")
		

GetData(CNN).scrape()

