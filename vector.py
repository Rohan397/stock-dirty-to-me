from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, BSHTMLLoader


def initialize_vectore_store():
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    db_location = "./filings"
    vector_store = Chroma(
        collection_name="EDGAR_FILINGS",
        embedding_function=embeddings,
        persist_directory=db_location,
    )
    return vector_store


def add_chunks_to_vector_store(chunks, file, vector_store):
    for i, chunk in enumerate(chunks):
        chunk_id = f"{file}_chunk_{i}"

        chunk.metadata.update(
            {"source": file, "chunk_number": str(i)}
        )

        vector_store.add_documents(documents=[chunk], ids=[chunk_id])
    print(f"Completed: Added {str(i+1)} chunks from {file} to vector store")


def process_document(filename, vector_store):
    loader = BSHTMLLoader(filename)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(document)
    add_chunks_to_vector_store(chunks, filename, vector_store)


def get_retriever(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    return retriever
