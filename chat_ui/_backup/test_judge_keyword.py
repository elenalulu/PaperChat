# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd


query = 'what is Astro HEP BERT'
client = openai.OpenAI(
	base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
	api_key = "no-key-required"
)


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


root_dir = '../arxiv_pdf/'
for root, dirs, files in os.walk(root_dir):
	for filename in files:
		if filename == most_title + '.pdf':
			most_title_path = os.path.join(root,filename)
			print (most_title_path)

			total_content = ''
			with pdfplumber.open(most_title_path) as pdf:
				for page in pdf.pages: #加：判断和问题相关度
					wholepage = page.extract_text()
					wholepage = wholepage.replace('\n','').replace(' ','')
					if len(total_content) < 1000:
						total_content += wholepage + '\n'
					else:
						break

			content =  total_content + '。answer according to the above content：' + query

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

			print ('-------------')
			print (final_answer)