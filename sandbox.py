# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:03:30 2023

@author: Madeline

converts any file type to plain text
handles structured formatting like tables and subsections

"""
"""

# give the method a .dox file to convert to plain text
# https://python.langchain.com/docs/integrations/document_loaders/microsoft_word

from langchain.document_loaders import Docx2txtLoader

# convert docx file to text file

loader = Docx2txtLoader("proposal.docx")
data = loader.load()
with open(txt_file, 'w', encoding='utf-8') as f:
    f.write(data)
print(data)    
  

docx2text("proposal.docx", "test.txt")
"""

#from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup
import re
from langchain.docstore.document import Document

"""
loader = PyPDFLoader("RCIP.pdf")
pages = loader.load_and_split()
"""
structured_file = ".spyder-py3\pdf2txt_env"

loader = PDFMinerPDFasHTMLLoader(".spyder-py3\RCIP.pdf")
data = loader.load()[0]   # entire PDF is loaded as a single Document

soup = BeautifulSoup(data.page_content,'html.parser')
content = soup.find_all('div')

cur_fs = None
cur_text = ''
snippets = []   # first collect all snippets that have the same font size
for c in content:
    sp = c.find('span')
    if not sp:
        continue
    st = sp.get('style')
    if not st:
        continue
    fs = re.findall('font-size:(\d+)px',st)
    if not fs:
        continue
    fs = int(fs[0])
    if not cur_fs:
        cur_fs = fs
    if fs == cur_fs:
        cur_text += c.text
    else:
        snippets.append((cur_text,cur_fs))
        cur_fs = fs
        cur_text = c.text
snippets.append((cur_text,cur_fs))
# Note: The above logic is very straightforward. One can also add more strategies such as removing duplicate snippets (as
# headers/footers in a PDF appear on multiple pages so if we find duplicates it's safe to assume that it is redundant info)

cur_idx = -1
semantic_snippets = []
# Assumption: headings have higher font size than their respective content
for s in snippets:
    # if current snippet's font size > previous section's heading => it is a new heading
    if not semantic_snippets or s[1] > semantic_snippets[cur_idx].metadata['heading_font']:
        metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
        metadata.update(data.metadata)
        semantic_snippets.append(Document(page_content='',metadata=metadata))
        cur_idx += 1
        continue
    
    # if current snippet's font size <= previous section's content => content belongs to the same section (one can also create
    # a tree like structure for sub sections if needed but that may require some more thinking and may be data specific)
    if not semantic_snippets[cur_idx].metadata['content_font'] or s[1] <= semantic_snippets[cur_idx].metadata['content_font']:
        semantic_snippets[cur_idx].page_content += s[0]
        semantic_snippets[cur_idx].metadata['content_font'] = max(s[1], semantic_snippets[cur_idx].metadata['content_font'])
        continue
    
    # if current snippet's font size > previous section's content but less than previous section's heading than also make a new 
    # section (e.g. title of a PDF will have the highest font size but we don't want it to subsume all sections)
    metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
    metadata.update(data.metadata)
    semantic_snippets.append(Document(page_content='',metadata=metadata))
    cur_idx += 1
    
#print(semantic_snippets)
with open(structured_file, 'w', encoding='utf-8') as f:
    f.write(str(semantic_snippets))
