import os
from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os
from dotenv import load_dotenv

load_dotenv()

def get_chatbot_chain():

    loader = MongodbLoader(
        connection_string="mongodb://localhost:27017/",
        db_name='local', 
        collection_name='products',
        field_names= ['brand', 'name', 'regular_price', 'sale_price', 'price_per_kg', 'price_per_unit', 'price_per_100ml', 'price_per_100g']
    )
    
    documents = loader.load()
    print(documents[0])


    vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(),
                                                  retriever=vectorstore.as_retriever(),
                                                  memory=memory)
    return chain