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
import nest_asyncio
import sys

nest_asyncio.apply()

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
multi_query_template = """Your task is to generate a question for each comma separated item in a grocery list provided  
to help retrieve relevant documents from a vector database with the goal of improving the search accuracy of their query. 
The questions should be phrased in a way that would help the user find the best deals on groceries, by asking which store has the best price for each item.
Price per kg, price per unit, price per 100g, and price per 100ml are all different ways to measure the price of a product, and the same unit of measurement should be used when comparing prices of similar products. 
The output should only include these questions separated by newlines. Include only as many questions as there are items on the list. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(multi_query_template)

generate_queries = (
prompt_perspectives 
| ChatOpenAI(model_name="gpt-3.5-turbo", top_p=0.05)
| StrOutputParser() 
| (lambda x: x.split("\n"))
)

classification_template = """
    you are a simple classification system given a list of uncategorized product listed below: 
    {context}
    Categorize each product as an item from the comma separated list in the question: {question}. 
    Every product needs to be assigned one category. Only use the items from the question as categories to categorize each product.

    the output for each product should be as follows:
    category: category, brand (if not empty): brand, name: name, store: store, sale price (if present): $price, regular price: $price, size: size, $price by kg, 100g, ml or unit. 
    separate each product by newlines
"""

classification_prompt=ChatPromptTemplate.from_template(classification_template)

documents = loader.load()

vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)

retriever=vectorstore.as_retriever()

retrieval_chain = generate_queries | retriever.map() | get_unique_union

triage_chain = (
{"context": retrieval_chain, "question": itemgetter('question')} 
| classification_prompt
| llm
| StrOutputParser()
)   


template = """
You are a grocery store app that helps users find the best deals on groceries. 
You are provided a list of products which include category, brand, name, store, price, price by kg, 100g, ml or unit in the context below:
{context}

Your goal is to give users the best recommendations of what products to buy from different stores based on price, so that they can save money. 
Price per kg, price per unit, price per 100g, and price per 100ml are all different ways to measure the price of a product, and the same unit of measurement should be used when comparing prices of products in the same category. 
Analyze all the products per category and determine which one to suggest based on the comparison methods listed above.
Favor the one with the lowest price by kg or by 100g first, then regular price. 
If the price by kg or by 100g is not available, use the price by unit. If the price by unit is not available, use the price by 100ml
If price by kg, by 100g or by 100ml is not available, use the regular price. Do not suggest more than 1 item per category.

The output should be in markdown format where the header is the store id and a list or products beneath the header of that store.

Example output:
### store 1
- brand name, size, $sale price (if exists), $ price, $ price by kg or by 100g or unit, or by 100ml
"""

final_prompt = ChatPromptTemplate.from_template(template)
llm=ChatOpenAI(model_name="o3-mini", reasoning_effort="high")

final_chain = (
{"context": triage_chain} 
| final_prompt
| llm
| StrOutputParser()
)   

while True:
    query = input('Give me a shopping list  (or type "exit" to quit): ')

    if query == "exit":
        print('Exiting')
        sys.exit()

    response = final_chain.invoke({"question":query})

    print(response)


