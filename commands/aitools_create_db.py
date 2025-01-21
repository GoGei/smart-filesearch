from configs import settings
from aitools.processors import AIToolProcessor

AIToolProcessor.create_vectors(
    openai_embeddings=AIToolProcessor.get_openai_embeddings(),
    client_settings=AIToolProcessor.get_client_settings(),
    files_path=settings.AI_SOURCE_FILES_FULL,
    chunk_size=settings.AI_CHUNK_SIZE,
)
