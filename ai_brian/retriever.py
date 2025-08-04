#SoulTrak/ai_brain/retriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

# Load activity log
loader = CSVLoader(r"E:\Habit Tracker\SoulTrak\Data\Traker\trak.csv")  # Use relative path
docs = loader.load()

# Split for embedding
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_documents(docs)

# Embed + store
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(texts, embedding)

# Save
vectorstore.save_local(r"E:\Habit Tracker\SoulTrak\ai_brain\vectorstore")
