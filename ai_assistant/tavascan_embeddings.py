import os
import requests
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.vectorstores.base import VectorStoreRetriever


class CupraManualQA:
    def __init__(
        self,
        pdf_url: str,
        pdf_path: str = "cupra_manual.pdf",
        db_path: str = "./chroma_db",
        embedding_model: str = "nomic-embed-text",
    ):
        self.pdf_url = pdf_url
        self.pdf_path = Path(pdf_path)
        self.db_path = db_path

        self.embedding = OllamaEmbeddings(model=embedding_model)

        # Load or create the vector store
        if Path(self.db_path).exists():
            print("✅ Loading existing Chroma DB...")
            self.vectorstore = Chroma(persist_directory=self.db_path, embedding_function=self.embedding)
        else:
            print("📥 DB not found. Creating new vectorstore...")
            self._download_pdf()
            self._process_pdf()

        self.retriever: VectorStoreRetriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def _download_pdf(self):
        if not self.pdf_path.exists():
            print(f"⬇️ Downloading PDF from {self.pdf_url}...")
            response = requests.get(self.pdf_url)
            with open(self.pdf_path, "wb") as f:
                f.write(response.content)
        else:
            print("📄 PDF already exists locally.")

    def _process_pdf(self):
        print("🔍 Loading and splitting PDF...")
        loader = PyPDFLoader(str(self.pdf_path))
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)

        print("🧠 Generating embeddings and creating Chroma DB...")
        self.vectorstore = Chroma.from_documents(chunks, self.embedding, persist_directory=self.db_path)
        #self.vectorstore.persist()
        print("✅ Chroma DB created and persisted.")

    def search(self, query: str, top_k: int = 3):
        """Return top_k most relevant chunks for the query."""
        results = self.retriever.invoke(query)
        ret =  [doc.page_content for doc in results]
        if ret:
            return ret [0:min(2, len(ret))]
        else:
            return []
