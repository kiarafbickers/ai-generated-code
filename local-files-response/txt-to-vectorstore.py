from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, ChromaDB
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
import magic
import os
import nltk

os.environ["OPENAI_API_KEY"] = "my_key"

loader = DirectoryLoader('store', glob='**/*.txt')
docs = loader.load()

char_text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
doc_texts = char_text_splitter.split_documents(docs)

openAI_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
vStore = Chroma.from_documents(doc_texts, openAI_embeddings)

# define the query vector
query = openAI_embeddings.embed_query("What are the effects of homelessness")

try:
    # request up to 4 results from the index
    results = vStore.get_nns_by_vector(query, 4)
except ChromaDB.errors.NotEnoughElementsException:
    # handle the error gracefully
    num_elements = vStore.index.get_n_elements()
    print(f"Error: only {num_elements} elements in index, requested 4 results")
    results = vStore.get_nns_by_vector(query, num_elements)

# print the results
print(results)
