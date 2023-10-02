import os
os.environ["COHERE_API_KEY"] = "9T7g3ZJ4d49BMk5MceXcYFnwD5KdarAFlieCn8Vc"
os.environ["OPEN_API_KEY"] = "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"


# Import some stuff
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.retrievers import BM25Retriever
from langchain.retrievers.merger_retriever import MergerRetriever
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain.document_loaders import PyPDFLoader

import os
COHERE_API_KEY = "9T7g3ZJ4d49BMk5MceXcYFnwD5KdarAFlieCn8Vc"
OPEN_API_KEY = "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"

# we can set the Cohere API key as an environmental variable, there is a bug that makes this not work for OpenAI
import os
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

'''
# load a PDF documents into the Document format that we use downstream
loader = PyPDFLoader("RCIP.pdf")
text_data = loader.load_and_split()
'''

# This will use the unstructured library to fetch the Metamorphosis book webpage
loader = UnstructuredURLLoader(["https://www.gutenberg.org/cache/epub/5200/pg5200-images.html"])
# returns a list of langchain.schema.document.Document objects
text_data = loader.load()

# in this example, we try to make chunks with less than 500 tokens
# these chunks will overlap by 50 tokens.
text_splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=20)
# this creates a list of LangChain Document objects
chunks = text_splitter.split_documents(text_data)

embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)

db = Chroma.from_documents(chunks, embeddings)
# our search method will be cosine similarity, and it will return the 10 most similar docs
semantic_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})

# The BM25 retriever will return the 10 docs with the best lexical matches
bm25_retriever = BM25Retriever.from_documents(chunks, k=10)

# merge both retrievers into one. When you use the merged retrievers, a single list of chunks (docs)
# will be returned
merged_retriever = MergerRetriever(retrievers=[semantic_retriever, bm25_retriever])

# Create a query
my_query = "max allocation"
# grab only the most similar document
docs = db.similarity_search(my_query, k=1)
#print(docs[0].page_content)

# now let's try out the lexical retriever
bm25_retriever.get_relevant_documents(my_query)

# demonstrate that the merged retriever returns the expected number of results (20)
len(merged_retriever.get_relevant_documents(my_query))

# create a CohereRerank object that returns the 3 most relevant docs
# You must have the Cohere api key set for this to work
compressor = CohereRerank(top_n=3)
# it will use the compress the output of the merged retriever to only 3 docs
compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=merged_retriever)
    
model_name = "gpt-3.5-turbo"  # ChatGPT
llm = ChatOpenAI(openai_api_key=OPEN_API_KEY, model_name=model_name)


prompt_template = """

{context}

Use context provided above, try to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Return your response in JSON format, with the result being assigned to a field name "result". Also, the JSON must contain a field named "context" that contains the exact information from the context that most influenced your answer, word for word.
Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
# k is the number of relevant text chunks to return
qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 chain_type_kwargs=chain_type_kwargs,
                                 retriever=compression_retriever)


#my_query = "What is the most important rule that grant proposals must follow according to the RCIP?"

#result = qa({"query": my_query})
#print(result['result'])

prompt_template = """
Context:
{context}

Chat History:
{chat_history}

Using the context and chat history provided above, try to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Return your response in JSON format, with the result being assigned to a field name "result". Also, the JSON must contain a field named "context" that contains the exact information from the context that most influenced your answer, word for word.
Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question", "chat_history"]
)

# memory_key and input_key point to the prompt keys
chain_type_kwargs = {"prompt": PROMPT,"memory": ConversationBufferMemory(
            memory_key="chat_history",
            input_key="question")}
qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 chain_type_kwargs=chain_type_kwargs,
                                 retriever=compression_retriever,
                                 )

# let's ask the same question
my_query = "“What did Gregor want to turn his room into?"

result = qa({"query": my_query})
print(result['result'])

# and now let's ask a follow-up question that only makes sense if the LLM can access the chat history
result = qa({"query": "Why did he want to turn into that"})
print(result['result'])



