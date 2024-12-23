# coding: utf-8
import glob
from os.path import join
import os, re, shutil


root_dir = './paper_ai/'
# pdf_list = glob(join(root_dir, "*.pdf"))


pattern = f'{root_dir}/**/*.pdf'
pdf_list = glob.glob(pattern)



for pdf_path in pdf_list:
	done_path = pdf_path.replace('./paper_ai','./_backup/used_paper_ai')
  
	if not os.path.exists(done_path):
		# print (pdf_path)
		title = pdf_path.replace('./paper_ai\\cs_AI\\','').replace('.pdf','')
		print (title)
		