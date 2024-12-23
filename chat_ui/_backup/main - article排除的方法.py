# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime, shutil
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter


client = openai.OpenAI(
	base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
	api_key = "no-key-required"
)


def judge_chat(query):

	content =  query 
	completion = client.chat.completions.create(
	model="",
	messages=[
		{"role": "user", "content": content}
	]
	)
	output = completion.choices[0].message
	answer = re.findall(r"content='(.+?)'", str(output))
	answer = '' .join(answer)
	answer = str(answer)
	print (answer)

	if '否' not in answer:
		content =  '记住你现在的名字叫来藤。回答：' + query
		# print (content)

		completion = client.chat.completions.create(
		model="",
		messages=[
			{"role": "user", "content": content}
		]
		)
		output = completion.choices[0].message
		answer = re.findall(r"content='(.+?)'", str(output))
		answer = '' .join(answer)
		answer = str(answer)
		print (answer)
		judge_answer = answer

	else:
		judge_answer = '否'

	return judge_answer



def language_qa(query): 
	final_answer = ''
	http_pdf = ''
		
	#判断哪篇paper
	content =  query + '. give the keyword of the above query as the format:keyword1&keyword2&keyword3'
	completion = client.chat.completions.create(
	model="",
	messages=[
		{"role": "user", "content": content}
	]
	)
	output = completion.choices[0].message
	answer = re.findall(r"content='(.+?)'", str(output))
	answer = '' .join(answer)
	answer = str(answer)
	answer = answer.lower()
	print (answer)


	keyword_csv = '../title_keyword.csv'
	df = pd.read_csv(keyword_csv)

	query_keyword_list = answer.split('&')
	title_keyword_total = []
	for query_keyword in query_keyword_list:

		results = df[df['keyword'] == query_keyword]
		if 'Empty DataFrame' not in str(results):
			for i in range(0, len(results)):
				oneline = results[i:(i+1)]
				title = oneline['title'].values 
				title = ''.join(title)

				title_keyword_dict = {'title': title, 'keyword': query_keyword}
				title_keyword_total.append(title_keyword_dict)
				

	counts = Counter([item['title'] for item in title_keyword_total])

	
	most_title = counts.most_common(1)
	most_title = most_title[0]
	most_title = str(most_title).split("',")
	most_title = most_title[0]
	most_title = most_title.replace("('",'')
	print (most_title)

	#查找most_title里所有的article
	results_title = df[df['title'] == most_title]
	if 'Empty DataFrame' not in str(results_title):
		total_article = ''

		for i in range(0, len(results_title),1):
			oneline = results_title[i:(i+1)]
			category = oneline['category'].values 
			category = ''.join(category)
			article = oneline['article'].values 
			article = ''.join(article)
			total_article += article	

		content =  total_article + '。answer according to the above content：' + query
		completion = client.chat.completions.create(
		model="",
		messages=[
			{"role": "user", "content": content}
		]
		)
		output = completion.choices[0].message
		answer = re.findall(r"content='(.+?)'", str(output))
		answer = '' .join(answer)
		answer = str(answer)

		if answer != '':
			final_answer =  answer.replace('\\n','<br>')

		print ('-------------')
		print (final_answer)

		http_pdf = 'https://s10.z100.vip:16418/arxiv_pdf/' + category + '/' + most_title + '.pdf'

	return final_answer, http_pdf


def internet_result(query):
	output = ''

	#baidu搜索
	url = 'https://www.baidu.com/s'
	param = {
		'wd':query #搜索词
	}
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
	}
	res = requests.get(url = url, params = param, headers = headers)
	res.encoding = 'utf-8'
	# print (res.text)

	beautisoup = BeautifulSoup(res.text,"lxml")
	results = beautisoup.find_all('div',class_="c-container")

	count = 0
	output = ''
	baidu_list = []
	for result in results:
		#6天前这种剔除了，可以考虑加进来
		if count<10 and '股票行情' not in str(result) and '<div class="c-container"' in str(result) and '<div class="result c-container' not in str(result):
			result = str(result).replace('\n','')

			description = re.findall(r'data-tools=(.+?)id=', result)
			description = ''.join(description)
			title = re.findall(r'title(.+?)url', str(description))
			title = ''.join(title)
			title = re.sub("<[^>]*?>","", title)
			title = title.replace(' ','').replace('":"','').replace('","','').replace("': &quot;","&quot;,'").replace("':&quot;","").replace("&quot;,'","")

			content = re.findall(r'"contentText":"(.+?)"', result)
			content = ''.join(content)
			content = re.sub("<[^>]*?>","", content)

			if '"url":"http' in str(description):
				url = re.findall(r'"url":"(.+?)"', str(description))
				url = ''.join(url)
			else:
				url = re.findall(r"url':(.+?)}", str(description))
				url = ''.join(url)
			url = url.replace(' ','').replace("&quot;","").replace(";","")

			if '"newTimeFactorStr":""' in str(result) or '天前' in str(result):
				timestamp = 0 
			else:
				date = re.findall(r'"newTimeFactorStr":"(.+?)日', str(result))
				date = ''.join(date)
				date = '头' + date + '日'

				year = re.findall(r'头(.+?)年', str(date))
				year = ''.join(year)
				year = int(year)
				month = re.findall(r'年(.+?)月', str(date))
				month = ''.join(month)
				month = int(month)
				day = re.findall(r'月(.+?)日', str(date))
				day = ''.join(day)
				day = int(day)
				date_change = datetime.datetime(year, month, day)
				timestamp = date_change.timestamp()
			

			count += 1
			single_tuple = (timestamp, title, content, url)
			baidu_list.append(single_tuple)

	#按日期排序
	baidu_list.sort(key=lambda x:x[0], reverse=True)

	count_baidu = 0
	for item in baidu_list:
		if count_baidu < 3:
			title = item[1]
			content = item[2]
			url = item[3]
			output = output + '<strong>' + title + '</strong>' + '<br><br>' 
			output = output + content + '<br><br>'
			output = output + '<a href="' + url + '" target="_blank">点此链接查看详情<a><br><br><br>'
			count_baidu += 1

	return output



app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/qa")
def get_doc_response():
	query = request.args.get('msg')
	output, pdf_single = language_qa(query) #中英文都可以用
 
	#不止一篇paper回答


	#互联网查询
	internet = ''
	if pdf_single == 'none':
		internet = internet_result(query)

	return [output, pdf_single, internet]


		

if __name__ == "__main__":
	
	#show browser 
	os.system('"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" http://127.0.0.1:5501')

	#run 
	app.run(host="0.0.0.0", port=5501)