import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_collection(name="campaigns", embedding_function=ef)

def ask(question: str) -> str:
    collection = get_collection()
    
    # 1. Busca las 5 campañas más relevantes
    results = collection.query(query_texts=[question], n_results=5)
    context = "\n\n".join(results["documents"][0])
    
    # 2. Construye el prompt
    prompt = ChatPromptTemplate.from_template("""
    Eres un analista de marketing experto. Responde basándote SOLO en los datos 
    de campañas proporcionados. Sé conciso y usa números concretos.
    Si la información no está en los datos, dilo claramente.
    
    Datos relevantes:
    {context}
    
    Pregunta: {question}
    
    Respuesta:
    """)
    
    # 3. Llama al LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm
    
    response = chain.invoke({"context": context, "question": question})
    return response.content