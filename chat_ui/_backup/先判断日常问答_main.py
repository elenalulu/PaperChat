# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests


client = openai.OpenAI(
	base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
	api_key = "no-key-required"
)


def judge_chat(query):

	content =  query + '。判断上面的是日常对话吗。是的话直接输出回答，不是的话输出否'
	print (content)

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
	def get_files_list(directory):
		return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

	directory = './static/local_document/'   
	files_list = get_files_list(directory)

	final_answer = ''
	for each_pdf in files_list:
		print (each_pdf)

		with pdfplumber.open(each_pdf) as pdf:
			count = 0
			total_content = ''
			for page in pdf.pages: #加：判断和问题相关度
				print (page)
				count += 1
				wholepage = page.extract_text()
				wholepage = wholepage.replace('\n','').replace(' ','')

				if count <= 3:
					total_content += wholepage + '\n'
				else:
					break

	content =  total_content + '。answer according to the above content：' + query
	print (content)

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
		split_list = answer.split('.')
		revised_list = split_list[:-1]
		
		for item in revised_list:
			item = item.replace('\\n','<br>')
			final_answer =  final_answer + item + '.'

	return final_answer, each_pdf


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

	#判断对话
	judge_answer = judge_chat(query)
	if judge_answer != '否':
		output = judge_answer
		pdf_single = ''
	
	#文字理解
	else:
		output, pdf_single = language_qa(query)

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