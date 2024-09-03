import gradio as gr
import time
import openai
import os
from langchain.vectorstores import Chroma
from typing import List, Tuple
import re
import ast
import html
from models import *

class Chatbot : 
    @staticmethod
    def clean_references_vectordb(documents: List) -> str:
        documents = [str(x) + "\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        
        for doc in documents:
            try:
                # Attempt to extract content and metadata
                match = re.match(r"page_content='(.*?)'(?: metadata=\{(.*)\})?", doc, re.DOTALL)
                if not match:
                    raise ValueError(f"Document format not recognized: {doc[:100]}...")  # Show first 100 characters
                
                content, metadata = match.groups()

                # Initialize metadata dict
                metadata_dict = {}
                
                if metadata:
                    metadata_dict = ast.literal_eval(f"{{{metadata}}}")

                # Decode newlines and other escape sequences
                content = bytes(content, "utf-8").decode("unicode_escape")

                # Replace escaped newlines with actual newlines
                content = re.sub(r'\\n', '\n', content)
                # Remove special tokens
                content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
                # Remove any remaining multiple spaces
                content = re.sub(r'\s+', ' ', content).strip()

                # Decode HTML entities
                content = html.unescape(content)

                # Replace incorrect unicode characters with correct ones
                content = content.encode('latin1').decode('utf-8', 'ignore')

                # Remove or replace special characters and mathematical symbols
                content = re.sub(r'â', '-', content)
                content = re.sub(r'â', '∈', content)
                content = re.sub(r'Ã', '×', content)
                content = re.sub(r'ï¬', 'fi', content)
                content = re.sub(r'â', '∈', content)
                content = re.sub(r'Â·', '·', content)
                content = re.sub(r'ï¬', 'fl', content)

                # Construct source and page number metadata (with defaults if missing)
                source = metadata_dict.get('file_name', 'Unknown source')
                page_number = metadata_dict.get('page_number', 'Unknown page')

                # Append cleaned content to the markdown string with two newlines between documents
                markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                    f"Source: {os.path.basename(source)} | Page number: {str(page_number)}\n\n"
                counter += 1
                
            except Exception as e:
                print(f"Error processing document {counter}: {e}")
                continue
        
        return markdown_documents
    @staticmethod
    def respond(chatbot: List, message: str, data_type: str = "Preprocessed doc", temperature: float = 0.0) -> Tuple:
        vectordb = Chroma(persist_directory='./data/vectordb',
                                  embedding_function=embedding)
        docs = vectordb.similarity_search(message, k=k)
        print(docs)
        question = "# User new question:\n" + message
        retrieved_content = Chatbot.clean_references_vectordb(docs)
        # Memory: previous two Q&A pairs
        chat_history = f"Chat history:\n {str(chatbot[-2:])}\n\n"
        prompt = f"{chat_history}{retrieved_content}{question}"
        print("========================")
        print(prompt)
        response =client.chat.completions.create(
            model=llm_engine,
            messages=[
                        {"role": "system", "content": llm_system_role},
                        {"role": "user", "content": prompt}
                    ],
            temperature=0,
            )

        chatbot.append(
            (message, response.choices[0].message.content))
        time.sleep(2)

        return "", chatbot, retrieved_content
    

    
    