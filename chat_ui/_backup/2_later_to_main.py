# coding: utf-8
import pandas as pd




corpus_file = 'paper_title_keyword.csv'
df = pd.read_csv(corpus_file)
# print (df)
# print (df['title'])

title = '_Sentiment_Analysis_Based_on_RoBERTa_for_Amazon_Review_An_Empirical_Study_on_Decision_Making'
results = df[df['title'] == title]

# print (results)
if 'Empty DataFrame' not in str(results):
	for i in range(0, len(results)):
		oneline = results[i:(i+1)]
		keyword = oneline['keyword'].values 
		keyword = ''.join(keyword)
		print (keyword)