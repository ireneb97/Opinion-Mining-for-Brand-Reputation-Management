import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import csv
import numpy as np
import re
import random
from bs4 import BeautifulSoup
import urllib.request as urllib2
import httplib2
import time
import csv

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

class review_builder:
	def __init__(self, name, score, title,place,date,verified_purch,text,upvotes):
		self.name = name
		self.score = score
		self.title = title
		self.place = place
		self.date = date
		self.verified_purch = verified_purch
		self.text = text
		self.upvotes = upvotes

def scraping(webpage):
	server = httplib2.Http(".cache")
	request_status, content = server.request(webpage)
	name_users_arr = []
	score_review_arr = []
	title_review_arr = []
	date_review_arr = []
	verified_purch_review_arr = []
	text_review_arr = []
	upvotes_review_arr = []
	reviews = []

	soup = BeautifulSoup(content,"html.parser")
	
	for i,review in enumerate(soup.findAll("div", {"class": 'a-section review aok-relative'})):
		if(review.find(class_='a-size-base review-text review-text-content') is not None and len(review.find(class_='a-size-base review-text review-text-content').text) !=0):
			found = False
			if(review.find(class_='a-profile-content') is not None):
				name_user = review.find(class_='a-profile-content').text
			else: 
				name_user = "unknown"	
			for j in range(1,6):
				class__ = 'a-icon a-icon-star a-star-' +str(j)+' review-rating'
				if(review.find(class_=class__) is not None): 
					score_review = review.find(class_=class__).text
					found = True
					break
			if(found==False): score_review = "no score found"
			if(review.find(class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold') is not None): 
				title_review = review.find(class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold').text.encode("utf-8-sig").decode()
				title_review = title_review.replace('\n','')
				title_review = remove_emojis(title_review)
			else: 
				title_review = "title not found"
			if(review.find(class_='a-size-base a-color-secondary review-date') is not None):
				date_review = review.find(class_='a-size-base a-color-secondary review-date').text
				a = date_review.split(',')
				b = a[0].split('on ')
				c = b[0].split('in ')
				place_review = c[1]
				date_review = b[1] + a[1]
			else: 
				place_review = "place not found"
				date_review = "date not found"

			if(review.find(class_='a-size-mini a-color-state a-text-bold') is not None and len(review.find(class_='a-size-mini a-color-state a-text-bold').text) != 0):
				verified_purch_review = review.find(class_='a-size-mini a-color-state a-text-bold').text
			else: 
				verified_purch_review = "purchase not verified"
			
			text_review = review.find(class_='a-size-base review-text review-text-content').text.encode("utf-8-sig").decode()
			text_review = text_review.replace('\n','')
			text_review = remove_emojis(text_review)

			if(review.find(class_='a-row a-spacing-small') is not None and len( review.find(class_='a-row a-spacing-small').text ) != 0):
				upvotes_review = review.find(class_='a-row a-spacing-small').text
			else: 
				upvotes_review = "0 people found this helpful"
			review = review_builder(name_user, score_review, title_review, place_review, date_review, verified_purch_review, text_review, upvotes_review)	
			reviews.append(review)
	return reviews


def multiple_scrap(incipit_path, number_pages,idle,verbosity=1):
	total_reviews = []
	reviews = []
	for i in range(1,number_pages+1):
		suffix = 'ref=cm_cr_getr_d_paging_btm_next_'+str(i)+'?ie=UTF8&reviewerType=all_review&pageNumber='+str(i)
		full_path = incipit_path + suffix
		reviews = scraping(full_path)
		total_reviews += reviews
		if(verbosity==2): print("scraped the " + str(i)+"th page. Other "+ str(number_pages-i) + " remaining!")
		if(number_pages>1): time.sleep(idle)	# sleep 30 sec between a scrap and another. Time complexity = idle * number_pages !!
	if(verbosity==1):print("scraped a total of "+ str(len(total_reviews)) + " reviews from amazon!")
	return total_reviews


def scrape_products_review_from_amazon(diff_paths,csv_file_names,number_pages,idle, verbosity=1):
	# diff paths: list of prefix links of the products

	# csv_file_names: list of string names as we want to save the file into(must be csv files!)

	# number_pages: number of pages we want to scrape for each product review

	# idle: time to wait between a page request and another. DO NOT SET IT TOO LOW,OR U MAY GET BANNED!
	
	#  verbosity: 
	# = 0 -> no prints; 
	# = 1 -> print only total number scraped per product;
	# = 2 -> print total number scraped per product plus a progression update for each.
	
	for i,path in enumerate(diff_paths):
		scraped_reviews = multiple_scrap(path,number_pages,idle,verbosity)
		with open(csv_file_names[i], 'w',encoding='utf-8-sig',errors='replace') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['name', 'score','title','place','date','verified purch', 'text', 'upvotes'])
			for review in scraped_reviews:
				writer.writerow([review.name, review.score, review.title, review.place, review.date, review.verified_purch, review.text, review.upvotes])




incipit_path_ps4 = 'https://www.amazon.com/PlayStation-4-Slim-1TB-Console/product-reviews/B071CV8CG2/'
incipit_path_ps5 = 'https://www.amazon.com/PlayStation-5-Console/product-reviews/B08FC5L3RG/'
incipit_path_Xbox1S = 'https://www.amazon.com/Xbox-One-S-1TB-Console-Discontinued/product-reviews/B073858Q9X/'
incipit_path_Xbox_series_X = 'https://www.amazon.com/Xbox-X/product-reviews/B08H75RTZ8/'


diff_paths = [incipit_path_ps5, incipit_path_Xbox1S, incipit_path_Xbox_series_X]
csv_file_names = ['scraped_reviews_ps5.csv','scraped_reviews_Xbox1_S.csv','scraped_reviews_Xbox_series_X.csv']
number_pages = 0
idle = 5



scrape_products_review_from_amazon(diff_paths=diff_paths, csv_file_names=csv_file_names, number_pages=number_pages, idle=idle, verbosity=2)



# setting the paths to each product,and storing them on an list, will prepare you to scrape the page. This code is a perfectly working scraping code
# for scraping amazon products. You actually have to past not the WHOLE link,but just the unique part(the so called incipit,in this code). 
# Example:
# total link = https://www.amazon.com/PlayStation-4-Slim-1TB-Console/product-reviews/B071CV8CG2/ref=cm_cr_getr_d_paging_btm_next_1?ie=UTF8&reviewerType=all_review&pageNumber=1
# incipit:  https://www.amazon.com/PlayStation-4-Slim-1TB-Console/product-reviews/B071CV8CG2/	<-- this is what you want to store in the list!
# suffix : ref=cm_cr_getr_d_paging_btm_next_1?ie=UTF8&reviewerType=all_review&pageNumber=1

