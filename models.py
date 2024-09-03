from dotenv import load_dotenv
import os ,getpass
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
# Load .env file
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")




embedding_model_engine = "text-embedding-ada-002"



embedding = OpenAIEmbeddings()


llm_engine= "gpt-3.5-turbo"


llm_system_role=  '''You are a chatbot. You'll receive a prompt that includes a chat history, retrieved content from the vectorDB based on the user's question, and the source.\ 
    Your task is to respond to the user's new question using only the information from the vectorDB without relying on your own knowledge.\
    you will receive a prompt with the the following format:

    # Chat history:\n
    [user query, response]\n\n

    # Retrieved content number:\n
    Content\n\n
    Source\n\n

    # User question:\n
    New question
    '''


client = OpenAI()

k=3

number_of_q_a_pairs: 2
