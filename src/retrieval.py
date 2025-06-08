import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from src.file_loader import all_splits, all_splits_2

os.environ["GOOGLE_API_KEY"] = "AIzaSyBr2cO37fWQbCifdkfCjD4sii21dfe1X88"
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

faiss_db = FAISS.from_documents(all_splits, embedding=embedding_model)
retriever = faiss_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 10
    }
)

faiss_db_2 = FAISS.from_documents(all_splits_2, embedding=embedding_model)
retriever_2 = faiss_db_2.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 10
    }
)