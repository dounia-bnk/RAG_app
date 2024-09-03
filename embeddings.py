from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
#from langchain.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from models import embedding_model_engine,embedding
import os

# Define the text splitter with your configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=500,
    length_function=len,
    is_separator_regex=["\n\n", "\n", " ", ""],
)


def load_documents(folder_path='./data/docs'):
    pdf_documents = []
    
    # List all files in the directory
    for file_name in os.listdir(folder_path):
        # Check if the file is a PDF
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Use PyPDFLoader to load the PDF
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                
                for i, doc in enumerate(documents):
                    # Attach metadata such as file name and approximate page number
                    doc.metadata = {
                        "file_name": file_name,
                        "page_number": i + 1  # Assuming each `doc` corresponds to a different page
                    }
                
                pdf_documents.extend(documents)  # Add all loaded documents to the list
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
    
    return pdf_documents 

# The chunk_documents and create_save_vectordb functions remain the same as before

def chunk_documents(docs: list):
    print('Chunking documents ...')
    chunked_docs = text_splitter.split_documents(docs)
    
    # Attach metadata to each chunk
    for chunk in chunked_docs:
        chunk.metadata['chunk_id'] = f"chunk_{chunk.metadata['page_number']}_{chunk.metadata['file_name']}"
    
    return chunked_docs

def create_save_vectordb():
    docs = load_documents()
    chunked_documents = chunk_documents(docs)
    
    print("Preparing vectordb...")
    
    vectordb = Chroma(
    embedding_function=embedding,
    persist_directory='./data/vectordb',  
)

    max_batch_size = 166

    for i in range(0, len(chunked_documents), max_batch_size):
        batch = chunked_documents[i:i + max_batch_size]
        vectordb.add_documents(documents=batch)
    
    print("VectorDB is created and saved.")
    print("Number of vectors in vectordb:", vectordb._collection.count(), "\n\n")
    return vectordb

create_save_vectordb()



