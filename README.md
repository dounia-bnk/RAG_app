**Predictive Maintenance RAG Chatbot**
This repository contains a Retrieval-Augmented Generation (RAG) system built using LangChain, ChatGPT, and Gradio. The project leverages a set of PDFs focused on predictive maintenance, transforming them into a knowledge base for a conversational AI model.
The system utilizes the following key components:
- PDF Documents: Source materials delving into predictive maintenance.
- LangChain: Framework used to manage and streamline the interaction between the documents, the vector database, and the language model.
- Chroma Vector Database: Stores the embeddings created from the PDFs, enabling efficient retrieval of relevant information.
- ChatGPT: The language model used to generate responses based on the retrieved information.
- Gradio: Provides an intuitive interface for interacting with the chatbot.
**Features**
Embeddings Creation: The project processes the PDF documents to create embeddings, capturing the semantic meaning of the content.
Vector Database: Embeddings are stored in a Chroma vector database, allowing for efficient retrieval of relevant document sections.
Conversational AI: The embeddings are fed into a ChatGPT model, enabling the chatbot to provide accurate and contextually relevant answers.
User Interface: Gradio is used to create a simple, user-friendly interface for interacting with the chatbot.
