# coding: utf-8
import glob
import os, re, time
import pdfplumber
import openai
import pandas as pd



root_dir = './paper_ai/'
pattern = f'{root_dir}/**/*.pdf'
pdf_list = glob.glob(pattern)


total_keyword = ''
for pdf_path in pdf_list:
	#先读了判断是否存在title
	df = pd.read_csv(data_csv_path)
	titles = df['title']
	print(titles)