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


query = '什么是astro hep bert'
query = 'what is bert'

#which paper
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


keyword_csv = '../label_keyword.csv'
df = pd.read_csv(keyword_csv)

query_keyword_list = answer.split('&')
label_keyword_total = []
for query_keyword in query_keyword_list:

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
print (most_label)


#request content
http_pdf = 'https://arxiv.org/pdf/' + most_label
print (http_pdf)

response = requests.get(http_pdf)
	 
page_contents = []
if response.status_code == 200:
    pdf_data = response.content
    pdf_document = fitz.open("pdf", pdf_data)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()  
        page_contents.append(text)


useful_articles = ''
for query_keyword in query_keyword_list:
	for article in page_contents:
		if query_keyword in article and article not in useful_articles:
			if len(useful_articles) < 3000: #control length
				useful_articles += article


content = useful_articles + '。answer according to the above content：' + query
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

print (final_answer)