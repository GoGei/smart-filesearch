import os
import shutil

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from chromadb.config import Settings

from configs import settings
from Utils.singleton import Singleton


class AIToolProcessor(Singleton):
    VECTORS = None

    def __init__(self,
                 files_path: str = settings.AI_SOURCE_FILES,
                 model_name: str = settings.AI_MODEL_NAME,
                 chunk_size: int = settings.AI_CHUNK_SIZE,
                 ):
        self.files_path = files_path
        self.model_name = model_name
        self.chunk_size = chunk_size

        if not os.path.exists(settings.AI_DB_DIR):
            self.qa_with_source = None
            return

        vector_store = self.load_vectors(
            openai_embeddings=self.get_openai_embeddings(),
            client_settings=self.get_client_settings(),
        )

        self.qa_with_source = RetrievalQAWithSourcesChain.from_chain_type(
            llm=ChatOpenAI(temperature=0,
                           model_name=self.model_name,
                           openai_api_key=settings.OPENAI_API_KEY),
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )
        setattr(AIToolProcessor, 'VECTORS', vector_store)

    @classmethod
    def get_openai_embeddings(cls) -> OpenAIEmbeddings:
        openai_embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        return openai_embeddings

    @classmethod
    def get_client_settings(cls) -> Settings:
        client_settings = Settings(
            chroma_db_impl="duckdb+parquet",  # we'll store as parquet files/DuckDB
            persist_directory=settings.AI_DB_DIR,  # location to store
            # anonymized_telemetr=False  # optional but showing how to toggle telemetry
        )
        return client_settings

    @classmethod
    def clear_db_store(cls):
        directory = settings.AI_DB_DIR
        try:
            shutil.rmtree(directory)
        except OSError as e:
            print('Error: %s - %s.' % (e.filename, e.strerror))

    @classmethod
    def create_vectors(cls,
                       openai_embeddings: OpenAIEmbeddings,
                       client_settings: Settings,
                       files_path: str = settings.AI_SOURCE_FILES_FULL,
                       chunk_size: int = settings.AI_CHUNK_SIZE,
                       ):
        print('AITools create vectors')
        print('Load documents from: %s' % files_path)
        doc_loader = DirectoryLoader(files_path)
        document = doc_loader.load()
        print('Documents loaded')
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        split_docs = text_splitter.split_documents(document)
        print('Split documents on chunks of size %s' % chunk_size)

        vector_store = Chroma.from_documents(split_docs, openai_embeddings,
                                             persist_directory=settings.AI_DB_DIR,
                                             client_settings=client_settings,
                                             collection_name='transcripts_store')

        print('Try to save documents to DB')
        vector_store.persist()
        print('Saved')
        return vector_store

    @classmethod
    def load_vectors(cls,
                     openai_embeddings: OpenAIEmbeddings,
                     client_settings: Settings,
                     ):
        print('AITools load vectors')

        vector_store = getattr(AIToolProcessor, 'VECTORS', None)
        if vector_store is not None:
            print('AITools already have initialized vectors')
            return vector_store

        print('AITools load vectors')
        vector_store = Chroma(collection_name='transcripts_store',
                              persist_directory=settings.AI_DB_DIR,
                              embedding_function=openai_embeddings,
                              client_settings=client_settings)

        setattr(AIToolProcessor, 'VECTORS', vector_store)
        return vector_store

    def process(self, question):
        return self.qa_with_source({"question": question})
