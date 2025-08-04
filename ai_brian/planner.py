#SoulTrak/ai_brain/planner.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import os
from dotenv import load_dotenv

load_dotenv()

# === Load Retriever ===
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("ai_brain/vectorstore", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# === Load LLM ===
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("API"),
    model_name="llama3-70b-8192"
)

def generate_output(selected_prompt: str) -> str:
    query = "my activity log"
    docs = retriever.get_relevant_documents(query)
    joined_context = "\n".join(doc.page_content for doc in docs)
    filled_prompt = selected_prompt.replace("{{context}}", joined_context)

    prompt = PromptTemplate.from_template(filled_prompt)
    chain: Runnable = prompt | llm
    return chain.invoke({})
