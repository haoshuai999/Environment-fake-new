import lxml
import requests
import csv
import random
import pandas as pd
import re
from lxml.html import fromstring

def scrape(url):
	user_agent_list = [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)",
		"AppleWebKit/537.36 (KHTML, like Gecko)",
		"Chrome/39.0.2171.95",
		"Safari/537.36"
	]


	headers = {
		'User-Agent': random.choice(user_agent_list)
	}
	# 	print(url)

	all_post_text = ""
	page_html_text = requests.get(url, headers=headers).text
	if re.search(r"File or directory not found", page_html_text):
		return "file not found"
	else:
		page_html = fromstring(page_html_text)

		origin_source = ""
		date = page_html.cssselect(".met .left span:not(a)")[0]
		date_text = date.text_content().split('/')[-1].strip()
		title = page_html.cssselect("h1")[0]
		title_text = title.text_content()
		author = page_html.cssselect(".met .left span a")[0]
		author_text = author.text_content().strip()
		main_body = page_html.cssselect(".awr p, .awr li, .awr h3")
		flag = 0
		for para in main_body:
			para_text = para.text_content().strip()
			if re.search(r"References", para_text):
				flag = 1
				continue
			if re.search(r"Books We Recommend", para_text) or re.search(r"[Pp]hoto [Cc]redit", para_text):
				break

			if flag == 0:
				all_post_text += para_text
			else:
				origin_source += para_text + '|'

		

		return (date_text, title_text, author_text, all_post_text, origin_source)

if __name__ == '__main__':
	# print(scrape("https://vactruth.com/2017/01/22/the-true-causes-of-sids/"))
	f = open("vactruth.txt", "r")
	urls = f.readlines()
	urls = [(line.rstrip('\n')) for line in urls]
	url_list = []
	date_list = []
	title_list = []
	author_list = []
	main_body_list = []
	origin_source_list = []

	count = 0
	for url in urls:
		count += 1
		if scrape(url) == "file not found":
			pass
		else:
			date, title, author, main_body, origin_source = scrape(url)
			url_list.append(url)
			date_list.append(date)
			title_list.append(title)
			author_list.append(author)
			main_body_list.append(main_body)
			origin_source_list.append(origin_source)
			if count % 200 == 0:
				print(count)
				print("output csv")
				df = pd.DataFrame(list(zip(url_list, date_list, title_list, author_list, main_body_list, origin_source_list)), columns=['URL', 'Date', 'Title', 'Author', 'Main-body', 'Origin-source'])
				df['Source'] = "vactruth"
				df.to_csv("vactruth.csv", index=False, encoding='utf-8-sig')

	df = pd.DataFrame(list(zip(url_list, date_list, title_list, author_list, main_body_list, origin_source_list)), columns=['URL', 'Date', 'Title', 'Author', 'Main-body', 'Origin-source'])
	df['Source'] = "vactruth"
	df.to_csv("vactruth.csv", index=False, encoding='utf-8-sig')
