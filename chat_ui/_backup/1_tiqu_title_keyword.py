# coding: utf-8
import glob
import os, re, time
import pdfplumber
import openai
import pandas as pd


client = openai.OpenAI(
	base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
	api_key = "no-key-required"
)


data_csv_path = 'paper_title_keyword.csv'


def tiqu_long():
	root_dir = './paper_ai/'
	pattern = f'{root_dir}/**/*.pdf'
	pdf_list = glob.glob(pattern)


	total_keyword = ''
	for pdf_path in pdf_list:
		#先读了判断是否存在title
		df = pd.read_csv(data_csv_path)

	  	#title
		title = pdf_path.replace('./paper_ai\\cs_AI\\','').replace('.pdf','')
		if title in str(df): 
			pass

		else:
			#keyword
			print (title)
			with pdfplumber.open(pdf_path) as pdf:
				total_content = ''
				for page in pdf.pages:
					print (page)
					wholepage = page.extract_text()
					wholepage = wholepage.replace('\n','').replace(' ','')

					content =  wholepage + '. give several keywords according to the above content, give output as format: keyworda&keywordb&keywordc'
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

					page_figure = str(page).replace('<Page:','').replace('>','')
					page_keyword = answer + '@page' + page_figure + '___'
					total_keyword += page_keyword

			#rank用时间戳
			current_timestamp = time.time()
			current_timestamp = str(current_timestamp).split('.')[0]
			rank = current_timestamp

			#title,keyword,rank
			single = '"' + title + '","' + total_keyword + '","' + rank + '"' + '\n\n'
			with open (data_csv_path,'a+',encoding='utf-8')as fl:
				fl.write(single)




if __name__ == '__main__':
	tiqu_long()