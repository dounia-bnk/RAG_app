from models import embedding, client , llm_engine, llm_system_role
from langchain.vectorstores import Chroma
from typing import List, Tuple
from chatbot import Chatbot
# Load the embedding function
embedding = embedding
# Load the vector database
vectordb = Chroma(persist_directory='./data/vectordb',
                  embedding_function=embedding)
#k number of similar chunks
k=3
# Prepare the RAG with openai in terminal
while True:
    question = input("\n\nEnter your question or press 'q' to exit: ")
    if question.lower() =='q':
        break
    question = "# user new question:\n" + question
    docs = vectordb.similarity_search(question, k=k)
    retrieved_content = Chatbot.clean_references_vectordb(docs)
    print(retrieved_content)
    #retrieved_docs_page_content: List[Tuple] = [
    #    str(x.page_content)+"\n\n" for x in docs]
    #retrived_docs_str = "# Retrieved content:\n\n" + str(retrieved_docs_page_content)
    #prompt = retrived_docs_str + "\n\n" + question
#
    #response =client.chat.completions.create(
    #model=llm_engine,
    #messages=[
    #            {"role": "system", "content": llm_system_role},
    #            {"role": "user", "content": prompt}
    #        ]
    #)
#
    #print(response.choices[0].message.content)