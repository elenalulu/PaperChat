import fitz 
import requests
 
# 从网络上获取PDF文件
url = 'https://pdf.dfcfw.com/pdf/H3_AP202412191641354785_1.pdf'

url = 'https://arxiv.org/pdf/2411.14877'
response = requests.get(url)
 
# 确保请求成功
if response.status_code == 200:
    # 打开一个PDF文档
    pdf_data = response.content
    pdf_document = fitz.open("pdf", pdf_data)
    
    # 读取PDF文档的内容
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()  # 获取页面文本内容
        print(f"Page {page_num + 1}:\n{text}")
 
    # 关闭PDF文档
    pdf_document.close()
# else:
#     print("Failed to download PDF")