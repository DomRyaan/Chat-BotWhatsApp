import os 

from decouple import config

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from Embedding.CustomEmbenddings import CustomEmbenddings

os.environ['HUGGINGFACEHUB_API_TOKEN'] = config('HUGGINGFACEHUB_API_TOKEN')

if __name__ == '__main__':
    file_path = "/app/rag/data/GiSalgados.pdf"
    loader = PyPDFLoader(file_path=file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(
        documents=docs,
    )

    persist_directory = "/app/chroma_data"

    embedding = CustomEmbenddings(model="sentence-transformers/all-MiniLM-L6-v2", token=os.environ['HUGGINGFACEHUB_API_TOKEN'])
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(
        documents=chunks,
    )