# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, shutil
import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
from flask_caching import Cache


client = openai.OpenAI(
    base_url="http://localhost:8080/v1", 
    api_key = "no-key-required"
)



app = Flask(__name__)

#全局变量
http_pdf = ''
query_keyword_list = []
dialoge = ''
url_list = []

def pdf_url(query): 
    query = query.lower()
    query = query.replace("what's",'').replace('what','').replace('who','').replace('whose','').replace('whom','').replace('where','').replace('which','').replace('why','').replace('when','').replace('how','').replace('is','').replace('are','').replace('of','').replace('difference','').replace('tell','').replace('me','').replace('and','').replace('-',' ').replace('_',' ').replace('idea','').replace('old','').replace('new','')
    query_split = query.split(' ')

    # query_keyword_list = []
    global query_keyword_list
    not_list = []
    for single_word in query_split:
        if single_word != '':
            word_csv = '../keyword_knowledge.csv'
            df = pd.read_csv(word_csv)

            results = df[df['keyword'] == single_word]
            if 'Empty DataFrame' not in str(results):
                query_keyword_list.append(single_word)
                for i in range(0, len(results)):
                    oneline = results[i:(i+1)]
                    knowledge = oneline['knowledge'].values 
                    knowledge = ''.join(knowledge)
                    query_keyword_list.append(knowledge)
            else:
                not_list.append(single_word)

    for single_word in not_list:
        if single_word != '':
            query_keyword_list.append(single_word)

    query_keyword_list = query_keyword_list[0:3] #control keyword number

    keyword = ''
    for item in query_keyword_list:
        if 'keyword' not in item:
            item = item.replace('.','')
            keyword = keyword + item + '+'

    keyword = keyword.rstrip('+')
    print (keyword)

    #arxiv search
    url = 'https://arxiv.org/search/?query=' + keyword + '&searchtype=all&abstracts=show&order=&size=50'
    res = requests.get(url)
    res.encoding = 'utf-8'
    page = res.text
    beautisoup = BeautifulSoup(page,"lxml")
    arxiv_result = beautisoup.find_all('li',class_="arxiv-result")

    i = 0
    most_label = 'none'
    # url_list = []
    global url_list
    other_pdf = ''

    for i in range(0, min(4,len(arxiv_result))):
        result = arxiv_result[i]
        result = str(result).replace('\n','')
        biaoshi = re.findall(r'https://arxiv.org/pdf/(.+?)"', result)
        biaoshi = ''.join(biaoshi)
        if i == 0:
            most_label = biaoshi
        url_list.append(biaoshi)
        i += 1

    if most_label != 'none' and len(url_list) != 0:
        http_pdf = 'https://arxiv.org/pdf/' + most_label

        for k in range(0, min(3,len(url_list))):
            if k > 0:
                next_pdf = 'https://arxiv.org/pdf/' + url_list[k]
                single_pdf = '<a href="{}" target="_blank">{}</a>'.format(next_pdf, next_pdf)
                other_pdf += single_pdf + '\n'

        dialoge = 'please refer to the first paper→' + '<br>' + 'you can also click the next papers:<br>' + other_pdf

    else:
        http_pdf = 'none'
        dialoge = 'I find this in network->'


    return http_pdf, query_keyword_list, dialoge, url_list


def language_qa(query, query_keyword_list, url_list): 
    query = query.lower()
    final_answer = ''
    useful_sentence = ''
    
    total_list = []
    for i in range(0, len(query_keyword_list)):
        list_i = []

    for i in range(0, min(4,len(url_list))):
        if len(useful_sentence) < 6000: #control total length
            biaoshi = url_list[i]
            now_pdf = 'https://arxiv.org/html/' + biaoshi
            print (now_pdf)

            res = requests.get(now_pdf)
            res.encoding = 'utf-8'
            page = res.text

            soup = BeautifulSoup(page,"lxml")
            text = soup.get_text()
            text = text.lower()
                
            for i in range(0, len(query_keyword_list)):
                single_sentence = ''
                keyword_i = query_keyword_list[i]

                if keyword_i in text:
                    sentence_list = text.split('\n')
                    for sentence in sentence_list:
                        if keyword_i in sentence:

                            if sentence not in list_i and len(single_sentence) < 2000: #control single length
                                list_i.append(sentence)

                                if sentence not in total_list:
                                    total_list.append(sentence)
                                    for item in total_list:
                                        useful_sentence += item

                                for item in list_i:
                                    single_sentence += item

            
    content = useful_sentence + '。answer the following query according to the above content in medium sentences：' + query
    # print (content)

    completion = client.chat.completions.create(
    model="",
    messages=[
        {"role": "user", "content": content}
    ]
    )
    output = completion.choices[0].message
    answer = output.content
    answer = str(answer)

    if answer != '':
        final_answer =  answer.replace('\\n','<br>')

    return final_answer


def internet_result(query):
    output = ''

    #baidu search
    url = 'https://www.baidu.com/s'
    param = {
        'wd':query 
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
    title_list = []

    for result in results:

        if count<10:
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

            if title != '' and title not in title_list:
                count += 1
                single_tuple = (title, content, url)
                baidu_list.append(single_tuple)
                title_list.append(title)

    count_baidu = 0
    for item in baidu_list:
        if count_baidu < 3:
            title = item[0]
            content = item[1]
            url = item[2]
            output = output + '<strong>' + title + '</strong>' + '<br><br>' 
            output = output + content + '<br><br>'
            output = output + '<a href="' + url + '" target="_blank">点此链接查看详情<a><br><br><br>'
            count_baidu += 1

    return output




@app.route("/")
def home():
    return render_template("index.html")


@app.route("/url")
def get_pdf_url():
    query = request.args.get('msg')
    http_pdf, query_keyword_list, dialoge, url_list = pdf_url(query)

    internet = ''
    if http_pdf == 'none':
        internet = internet_result(query)

    return [http_pdf, query_keyword_list, dialoge, internet]


@app.route("/qa")
def get_doc_response():
    query = request.args.get('msg')
    

    if http_pdf != 'none':
        output = language_qa(query, query_keyword_list, url_list) 
    else:
        output = 'none'

    return [output]


        

if __name__ == "__main__":
    
    #show browser 
    os.system('"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" http://127.0.0.1:5501')

    #run 
    app.run(host="0.0.0.0", port=5501)