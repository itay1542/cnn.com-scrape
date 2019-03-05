#!usr/bin/env
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re

options = Options()
options.headless = True
url = 'https://edition.cnn.com/'
driver=webdriver.Firefox(options=options)

class getData:

	def __init__(self,url):
		self.url = url

	def scrape(self):	
		try:
			print("scraping www.cnn.com , please wait as it might take a while :)")	
			driver.get('https://edition.cnn.com/')
			element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))	
			source = driver.page_source
			soup = BeautifulSoup(source,'html.parser')
			article_links = []
			for ul in soup.find_all('ul'):
				if('Top' in str(ul.h2)):
					for li in ul.find_all('li'):
						article_links.append(li.find('a').get('href'))
			
			self.scrape_from_pages(article_links)

		except Exception as e:
			print e			

		finally:
			print 'done'
			driver.close()

		return ''			

	def scrape_from_pages(self,links):
		articles_array = []
		for link in links:
			driver.get('https://edition.cnn.com'+link)
			x = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
			source = driver.page_source
			soup = BeautifulSoup(source,'html.parser')
			title = soup.h1.string
			paragraph = ''
			img_links =[]
			for p in soup.find_all('p'):
				if(p.cite):
					paragraph=p.get_text()
			for img in  soup.find_all('img'):
				if "media__image media__image--responsive" in str(img) :
					img_links.append(img.get('src'))
			article = {
				"title" : title,
				"paragraph" : paragraph,
				"links" : img_links
			}
			articles_array.append(article)
		self.print_to_screen(articles_array)
		return 

	def print_to_screen(self,array):
		print("Top Articles: \n")
		for article in array:
			images=""
			for link in article['links']:
				if(not re.match('data:(.*)',link)):
					images+=link[2:] + "\n"


			print('\033[1m' + article['title'] + "\033[0m \n" + article['paragraph']+ " \nimages: \n"+images+ "\n \n")
		

getData(url).scrape()

