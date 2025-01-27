# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime, shutil
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
import fitz 


client = openai.OpenAI(
	base_url="http://localhost:8080/v1", 
	api_key = "no-key-required"
)


def pdf_url(query): 
	http_pdf = ''
		
	#which paper
	query = query.replace('what','').replace('which','').replace('when','').replace('how','').replace('is','').replace('are','')
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
	# print (answer)


	keyword_csv = '../label_keyword.csv'
	df = pd.read_csv(keyword_csv)

	query_keyword_list = answer.split('&')
	label_keyword_total = []
	for query_keyword in query_keyword_list:
		if query_keyword !='keyword' and query_keyword != 'query':
			results = df[df['keyword'] == query_keyword]
			if 'Empty DataFrame' not in str(results):
				for i in range(0, len(results)):
					oneline = results[i:(i+1)]
					label = oneline['label'].values 
					label = str(label)
					label = label.replace('[','').replace(']','')

					label_keyword_dict = {'label': label, 'keyword': query_keyword}
					label_keyword_total.append(label_keyword_dict)
					
	counts = Counter([item['label'] for item in label_keyword_total])

	most_label = counts.most_common(1)
	most_label = most_label[0]
	most_label = most_label[0]
	most_label = most_label.replace("'",'')

	#request content
	http_pdf = 'https://arxiv.org/pdf/' + most_label
	print (http_pdf)

	other_pdf = ''
	for i in range(0, len(counts)):
		j = i + 1
		most_label = counts.most_common(j)
		most_label = most_label[i]
		most_label = most_label[0]
		most_label = most_label.replace("'",'')

		#request content
		next_pdf = 'https://arxiv.org/pdf/' + most_label
		if 0 < i < 4:
			single_pdf = '<a href="{}" target="_blank">{}</a>'.format(next_pdf, next_pdf)
			other_pdf += single_pdf + '\n'

	dialoge = 'please refer to the first paper→' + '<br>' + 'you can also click the next papers:<br>' + other_pdf

	return http_pdf, query_keyword_list, dialoge, counts


def language_qa(query, query_keyword_list, counts): 
	final_answer = ''
	useful_sentence = ''

	for i in range(0, len(counts)):
		if i < 4:
			j = i + 1
			most_label = counts.most_common(j)
			most_label = most_label[i]
			most_label = most_label[0]
			most_label = most_label.replace("'",'')
			now_pdf = 'https://arxiv.org/pdf/' + most_label
			print (now_pdf)
			response = requests.get(now_pdf)
			print (response.status_code)

			try:
				response = requests.get(now_pdf)	 
				page_contents = []

				if response.status_code == 200:
				    pdf_data = response.content
				    pdf_document = fitz.open("pdf", pdf_data)
				    
				    for page_num in range(len(pdf_document)):
				        page = pdf_document.load_page(page_num)
				        text = page.get_text()  
				        page_contents.append(text)
			except:
				pass

		for query_keyword in query_keyword_list:
			for article in page_contents:
				if query_keyword in article:
					sentence_list = article.split('\n')
					for sentence in sentence_list:
						if query_keyword in sentence and sentence not in useful_sentence:
							if len(useful_sentence) < 10000: #control length
								useful_sentence += sentence
							else:
								break


	useful_sentence = useful_sentence.lower()
	content = useful_sentence + '。answer according to the above content：' + query
	print (content)

	completion = client.chat.completions.create(
	model="",
	messages=[
		{"role": "user", "content": content}
	]
	)
	output = completion.choices[0].message
	answer = str(output).replace('ChatCompletionMessage(content="','').replace("role='assistant', function_call=None, tool_calls=None)",'').replace('",','')
	answer = '' .join(answer)
	answer = str(answer)

	if answer != '':
		final_answer =  answer.replace('\\n','<br>')

	return final_answer


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



@app.route("/url")
def get_pdf_url():
	query = request.args.get('msg')
	http_pdf, query_keyword_list, dialoge, counts = pdf_url(query)

	internet = ''
	if http_pdf == 'none':
		internet = internet_result(query)

	return [http_pdf, query_keyword_list, dialoge, internet]



@app.route("/qa")
def get_doc_response():
	query = request.args.get('msg')
	http_pdf, query_keyword_list, dialoge, counts = pdf_url(query)
	output = language_qa(query, query_keyword_list, counts) 

	return [output]


		

if __name__ == "__main__":
	
	#show browser 
	os.system('"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" http://127.0.0.1:5501')

	#run 
	app.run(host="0.0.0.0", port=5501)