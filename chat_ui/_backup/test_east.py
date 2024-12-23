import requests
from PyPDF2 import PdfReader
from io import BytesIO


# https://pdf.dfcfw.com/pdf/H3_AP202412191641354785_1.pdf
most_label = 'AP202412191641354785'
http_pdf = 'https://pdf.dfcfw.com/pdf/H3_' + most_label + '_1.pdf'
print (http_pdf)

response = requests.get(http_pdf)
response.encoding = response.apparent_encoding
print (response)
print (response.text)

# res = requests.get(http_pdf)
# res.encoding = 'utf-8'
# whole_pdf = res.text
# print (whole_pdf)


if response.status_code == 200:
    # 使用BytesIO将响应的内容当作文件对待
    pdf_file = BytesIO(response.content)
    reader = PdfReader(pdf_file)
    
    # 提取PDF文本（不转换编码）
    text = reader.get_pages(0)[0].extract_text()
    print(text)
else:
    print("请求PDF文件失败")