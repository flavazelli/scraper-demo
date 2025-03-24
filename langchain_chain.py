from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.load import dumps, loads
from operator import itemgetter
import sys

import os

load_dotenv()

def get_unique_union(documents: list[list]):
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]

loader = MongodbLoader(
    connection_string="mongodb://localhost:27017/",
    db_name='local', 
    collection_name='products',
    field_names= ['human_readable'],
    metadata_names= ['brand', 'name', 'regular_price', 'sale_price', 'price_per_kg', 'price_per_unit', 'price_per_100ml', 'price_per_100g']
)

# Multi Query: Different Perspectives
multi_query_template = """You are an AI language model assistant. Your task is to generate a question for each comma separated item in a grocery list provided  
to help retrieve relevant documents from a vector database with the goal of improving the search accuracy of their query. 
The output should only include these questions separated by newlines. Include only as many questions as there are items on the list. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(multi_query_template)

generate_queries = (
prompt_perspectives 
| ChatOpenAI(temperature=0) 
| StrOutputParser() 
| (lambda x: x.split("\n"))
)

template = """
You are a grocery store app that helps users find the best deals on groceries. 
You have access to a database of grocery products from different stores. 
Your goal is to give users the best recommendations of what products to buy from different stores based on price, so that they can save money. 
When a user asks which items are on sale, they are asking if there are any products that are currently being sold at a discounted price or at a sale price. Do your best to return items that have a sale price in this case. 
Make sure to always mention which store the item comes from to inform the user of where to shop by looking at the store id. 
Price per kg, price per unit, price per 100g, and price per 100ml are all different ways to measure the price of a product, and the same unit of measurement should be used when comparing prices of similar products. 
Favor the price by weight when available. If multiple similar items are available, favor the one with the lowest price by weight first, then regular price. 
If the price by weight is not available, use the price by unit. If the price by unit is not available, use the price by volume or weight.
If the price by volume or weight is not available, use the regular price.

The output should be in markdown format where the header is the store id and a list beneath the header of that store.
Only pick one product per item from the question in the output, even if there are multiple products that match the same item across different stores. 
Do not include products that were not asked for in the question.

Example output:
### store 1
- Item 1 - brand size, $ price, $ price by weight or unit
- Item 2 - brand size, $ price, $ price by weight or unit
### store 2
- Item 1 - size, $ price, $ price by weight or unit
- Item 2 - size, $ price, $ price by weight or unit

Answer the following question based on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

documents = loader.load()

vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

llm=ChatOpenAI(model_name="gpt-3.5-turbo")

retriever=vectorstore.as_retriever()

retrieval_chain = generate_queries | retriever.map() | get_unique_union

final_rag_chain = (
{"context": retrieval_chain, 
    "question": itemgetter('question')} 
| prompt
| llm
| StrOutputParser()
)   

while True:
    query = input('Prompt (or type "exit" to quit): ')

    if query == "exit":
        print('Exiting')
        sys.exit()

    response = final_rag_chain.invoke({"question":query})

    print(response)


