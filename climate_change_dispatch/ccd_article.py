import lxml
import requests
import csv
import random
import pandas as pd
import re
from lxml.html import fromstring

def scrape(url):
	user_agent_list = [
		"Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
		"Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
		"Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
		"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML, likeGecko)Chrome / 17.0.963.56Safari / 535.11",
		"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
		"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
	]


	headers = {
		'User-Agent': random.choice(user_agent_list)
	}
	# 	print(url)

	all_post_text = ""
	page_html_text = requests.get(url, headers=headers).text
	try:
		page_html_text = re.sub(r"<img class=\"(.*?)<\/noscript>", "", page_html_text)
	except:
		pass
	# print(page_html_text)
	page_html = fromstring(page_html_text)

	origin_source = ""
	author = page_html.cssselect(".tm-article-meta a")[0]
	author_text = author.text_content()
	date = page_html.cssselect(".tm-article-meta time")[0]
	date_text = date.text_content()
	title = page_html.cssselect(".tm-article-title")[0]
	title_text = title.text_content()
	main_body = page_html.cssselect(".tm-article-content >p")
	# print(main_body[0].text)
	for para in main_body:
		para_text = para.text_content().strip()
		if re.search(r"Read more", para_text):
			origin_source = re.sub(r"Read more at", "", para_text).strip()
		else:
			all_post_text += para_text
	
	# try:
	# 	main_post = page_html.cssselect(".topic-content p")[0]
	# 	main_post_text = main_post.text_content().strip()
	# except:
	# 	main_post_text = ''
	
	# try:
	# 	reply = page_html.cssselect(".reply-content")
	# 	for text in reply:
	# 		all_post_text.append(text.text_content().strip())
	# except:
	# 	reply = ''


	return (date_text, title_text, author_text, all_post_text, origin_source)

if __name__ == '__main__':
	# scrape("https://climatechangedispatch.com/11-million-jobs-at-risk-eu-green-deal/")
	f = open("ccd_article.txt", "r")
	urls = f.readlines()
	urls = [line.rstrip('\n') for line in urls]
	url_list = []
	date_list = []
	title_list = []
	author_list = []
	main_body_list = []
	origin_source_list = []

	count = 0
	for url in urls:
		count += 1
		date, title, author, main_body, origin_source = scrape(url)
		url_list.append(url)
		date_list.append(date)
		title_list.append(title)
		author_list.append(author)
		main_body_list.append(main_body)
		origin_source_list.append(origin_source)
		if count % 500 == 0:
			print(count)
			print("output csv")
			df = pd.DataFrame(list(zip(url_list, date_list, title_list, author_list, main_body_list, origin_source_list)), columns=['URL', 'Date', 'Title', 'Author', 'Main-body', 'Origin-source'])
			df['Source'] = "Climate Change Dispatch"
			df.to_csv("ccd_post.csv", index=False, encoding='utf-8-sig')

	df = pd.DataFrame(list(zip(url_list, date_list, title_list, author_list, main_body_list, origin_source_list)), columns=['URL', 'Date', 'Title', 'Author', 'Main-body', 'Origin-source'])
	df['Source'] = "Climate Change Dispatch"
	df.to_csv("ccd_post.csv", index=False, encoding='utf-8-sig')
