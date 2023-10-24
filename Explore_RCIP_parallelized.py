#!/usr/bin/env python
# coding: utf-8

# # TO DO:
# ## prompt to answer questions about the table

# In[1]:


import os
OPEN_API_KEY = "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"
os.environ["OPEN_API_KEY"] = OPEN_API_KEY

split_docs = []
split_docs2 = []

# In[2]:


table_prompt_initial = """
\n\n
<TABLE START>:
{table}
<TABLE END>:

The above text between "<TABLE START>" and "<TABLE END>" is a table formatted in plain language. It contains rows and columns and some rows may have more columns than others. Each row starts with "RX:" where "X" is the row number, starting at 0. Each column in each row starts with "CY:" where "Y" is the column number, starting at 0, followed by the text contained in the column, which is surrounded by quotation marks.\n\n
"""
def process_table(soup_table):
    """
    Function to convert an HTML table to a 2D Python list
    :param soup_table: The BeautifulSoup table element
    :return: A 2D Python list containing the tabular data
    """
    # This will contain our Table data
    data = []

    # See if this table has a header, and if so, add it to our data as the first row
    header = soup_table.find('thead')
    # grab all the headers, extract and clean the text, and add it to our data
    if header is not None:
        data.append([h.text.strip().replace('\xa0', ' ') for h in header.find_all('th')])

    # grab the main table body
    tbody = soup_table.find('tbody')
    if tbody is None:
        tbody = soup_table

    # get all rows
    rows = tbody.find_all('tr')

    # loop through every row
    for row in rows:
        # this will hold the data for this column
        col_data = []
        # check if there is a header, and if so, add it to the column data
        header = row.find('th')
        if header is not None:
            col_data.append(header.text.strip().replace('\xa0', ' '))

        # get al of the data columns for this row
        cols = row.find_all('td')

        # loop through each element in the column, clean it, and append to col_data
        for element in cols:
            element = element.text.strip()
            if element is None:
                col_data.append("N/A")
            else:
                element = element.replace('\xa0', ' ')
                col_data.append(element)
        # add the row to our data
        data.append(col_data)
    return data


# In[3]:


def table2text(table):
    """
    This function formats a table into a more human-readable format
    :param table: The table loaded from html, a 2D Python list
    :return: Formatted string
    """
    table_str = ""
    # loop through every row
    for i, row in enumerate(table):
        # indicate which row we are in
        table_str += "R{}: ".format(i)
        # loop through every column
        for j, column in enumerate(row):
            # indicate which column we are in
            table_str += 'C{}: "{}" '.format(j, column)
        # let's add a newline after the last column (probably not necessary)
        if i != len(table) - 1:
            table_str += '\n'
    return table_prompt_initial.format(table=table_str)


# In[4]:


# Import some stuff
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


# In[5]:


import re

# This list contains all of the HTML tags that contain text that we want to extract
# This excludes things like list items and tables, which are handled independently
text_containing_tags = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em',
    'blockquote', 'q', 'cite', 'abbr', 'code', 'pre', 'kbd', 'samp', 'var',
    'dfn', 'mark', 'ins', 'del', 'time', 'sub', 'sup'
]

def in_table(element):
    """
    Check if the current element is contained in a t
    
    able, in which case, it has already beeen processed
    :param element: Soup element
    :return: True if in table, False otherwise
    """
    # Loop through parent elements
    while element:
        if element.name in ['table',]:
            return True
        element = element.parent
    return False


# In[6]:


def process_element(element, text: str = "", verbose: bool = False):
    """
    Recursive function that iterates over all elements in the Soup HTML structure and extracts and formats text as prescribed for each type of HTML structure.

    NOTE: This function needs to be optimized.

    :param element: The soup element (typically the top-level element)
    :param text: The string that the function appends the results to
    :param verbose: True for verbosity, False otherwise
    :return: The extracted text as a String
    """
    # check if element has the name attribute. If it doesn't, it is a nonstandard tag that we want to ignore
    if element.name:
        # handle tables independently
        if element.name == 'table':
            if verbose:
                print("Handling table...")
            table_data = table2text(process_table(element))       
            text += table_data
            
        # handle plain text tags
        elif element.name in text_containing_tags:
            # check if this was in a table and thus already processed
            if not in_table(element):
                if verbose:
                    print("Handling text...")
                element_text = element.get_text()
                # ignore any text that is one character or less
                if len(element_text) > 1:
                    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        text += '\n\n'
                    # replace consecutive whitespace with a single space
                    text += re.sub(r'\s+', ' ', element_text)
                    text += ' '
                    text += '\n'
        # if we encountered a list item, then add in the list text (-, bullet point, etc.)
        elif element.name == 'li':
            if 'data-list-text' in element.attrs:
                text += element.attrs['data-list-text']
        # ignore table elements because they are already handled in the table handler
        elif element.name in ['td', 'tr']:
            pass
        # ignore the rest
        else:
            if verbose:
                print("Tag type not considered in loop: " + element.name)
    # recursively loop through the children of every element
    for child in element.find_all(recursive=False):
        text = process_element(child, text, verbose=verbose)
    if verbose:
        print("Done.")


    return text


# In[7]:


from bs4 import BeautifulSoup

# Generalized function to process any html file
def process_html(html_file: str) -> str:
    # open the file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_text = f.read()
    # Parse using BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')
    # Write the prettified HTML to a file so that we can look at it
    with open("pretty_%s" % html_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
        
    # format our document
    formatted_document = process_element(soup.find('body'), "", verbose=False)
    # write the results to a text file
    with open('formatted_%s.txt' % html_file[:-4], 'w', encoding='utf-8') as f:
        f.write(formatted_document)
        
    return formatted_document


# In[8]:


from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Generalized function to create list of split LangChain Document objects
def langchain_doc_splitter(formatted_document: str, overlap_percent: int=10) -> list:
    doc = Document(page_content=formatted_document)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=60000, chunk_overlap=60000*10/100)
    split_docs = text_splitter.split_documents([doc])
    
    return split_docs


# # Let's run each section of our double-RAG in parallel

# In[ ]:


from multiprocessing import Pipe
from multiprocessing import Process

# create function that runs above functions while providing connections to and from a multiprocessing Pipe
def data_preprocessor_pipeline(conn, html_file: str) -> None:
    # Get formatted data
    formatted_document = process_html(html_file)
    # Get split langchain document objects from formatted data
    split_docs = langchain_doc_splitter(formatted_document)
    # Send split document objects to the pipe
    conn.send(split_docs)
    conn.close()

# IMPORTANT TO-DO: add security authentication for recv/send methods
# IMPORTANT TO-DO: following code should be in an "if __name__ == '__main__':" block

if __name__ == '__main__':
    # Run the data preprocessing pipeline for the requirements html
    requirements_recv_conn, requirements_send_conn = Pipe()
    requirements_proc = Process(target=data_preprocessor_pipeline, args=(requirements_send_conn, 'RCIP2.html',))
    requirements_proc.start()

    # Run the data preprocessing pipeline for the proposal html
    proposal_recv_conn, proposal_send_conn = Pipe()
    proposal_proc = Process(target=data_preprocessor_pipeline, args=(proposal_send_conn, 'proposal.html',))
    proposal_proc.start()

    # Grab split documents output
    split_docs = requirements_recv_conn.recv()
    split_docs2 = proposal_recv_conn.recv()

    # Join the processes (memory cleaning)
    requirements_proc.join()
    proposal_proc.join()


# In[23]:


print(len(split_docs))


# # Let's use an OpenAI model

# In[10]:


model_name = "gpt-3.5-turbo-16k"  # ChatGPT
llm = ChatOpenAI(openai_api_key=OPEN_API_KEY, model_name=model_name, request_timeout=120)


# # Refine Summarization Chain

# In[11]:


from langchain.chains.summarize import load_summarize_chain
initial_template = """
I am writing a grant proposal and I would like to compare my proposal against the requirements set forth in the below text, nested between <TEXT> tags. Generate a comprehensive and specific overview of those requirements that will help me check my proposal. Your outline must be taken directly from the above text nested between the <TEXT> tags. If tabular data is important, include that too. If the provided information is insufficient to generate the outline, then do not do anything.
<TEXT>
{text}
<TEXT>
YOUR RESPONSE:"""
initial_prompt = PromptTemplate.from_template(initial_template)

refine_template = """
<TEXT>
{text}
<TEXT>
I am writing a grant proposal and I would like to compare my proposal against the requirements set forth in the below text, nested between <TEXT> tags. Generate a comprehensive and specific outline of the important requirements that will help me check my proposal for compliance against these requirements by refining the following text nested between <CURRENT OUTLINE> tags, which is an incomplete outline that you generated by processing portions of the grant requirements document. New information used to refine the incomplete outline must be taken directly from the above text nested between the <TEXT> tags. If tabular data is important, include that too. If the provided information is insufficient to refine the outline, then do not modify it.
<CURRENT OUTLINE>
{existing_answer}
<CURRENT OUTLINE>
YOUR RESPONSE:
"""
refine_prompt = PromptTemplate.from_template(refine_template)
chain = load_summarize_chain(
    llm=llm,
    chain_type="refine",
    question_prompt=initial_prompt,
    refine_prompt=refine_prompt,
    return_intermediate_steps=True,
    input_key="text",
    output_key="output_text",
)


# ## Generate Requirements Context from RCIP Docs

# In[12]:


result = chain({"text": split_docs}, return_only_outputs=True)
outline = result["output_text"]
print(outline)


# In[13]:


outline = Document(page_content=outline)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=60000, chunk_overlap=60000*10/100)
split_outline = text_splitter.split_documents([outline])
len(split_outline)
##SPLIT_OUTLINE IS THE RCIP REQUIREMENTS GENERATED BY THE 1ST RAG


# ## Now Identify Information from the Proposal related to the requirements context

# ## Prompt #2

# In[19]:


model_name = "gpt-3.5-turbo-16k"  # ChatGPT
llm2 = ChatOpenAI(openai_api_key=OPEN_API_KEY, model_name=model_name, request_timeout=120)


# In[20]:


from langchain.chains import LLMChain

template = """
<TEXT>
{text}
<TEXT>

<CONTEXT>
{input_documents}
<CONTEXT>

I am writing a grant proposal and I would like to compare my proposal document, which is nested between <TEXT> tags, against a set of requirements, which is nested between <CONTEXT> tags. I need to ensure that the content in the proposal meets the requirements. Go through each section of the proposal document, including sections A, B, C, D, E, F, G, H, and I, and tell me if each section meets the requirements. Describe why or why not each section meets the requirements. Specifically, first print the original section, then give your description of why or why not this section meets the requirements. If there are requirements that are not touched on in the proposal document, make note of that at the end of your output. If tabular data in the proposal document is important, check that against the requirements too. If the provided information is insufficient to generate an annotation of the proposal, then do not do it."

YOUR RESPONSE:
"""

prompt = PromptTemplate.from_template(template)

chain = load_summarize_chain(
    llm=llm2,
    chain_type="refine",
    question_prompt=prompt,
    return_intermediate_steps=True,
    output_key="output_text",
    input_key= "text",
)
    #input_key="input_documents",


# In[21]:


result = chain({ "text":split_outline, "input_documents":split_docs2}, return_only_outputs=True)
print(result["output_text"])


