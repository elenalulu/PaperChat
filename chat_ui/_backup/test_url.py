from urllib.request import urlopen

url = 'https://pdf.dfcfw.com/pdf/H3_AP202412191641354785_1.pdf'
html = urlopen(url)
output = html.read().decode("utf-8")
print (output)