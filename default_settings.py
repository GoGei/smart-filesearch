import os

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__))) + '/'

PROJECT_NAME = 'smart-filesearch'
SERVER_HOST = 'smart-filesearch'
SERVER_PORT = '4885'

# AI tools
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
AI_INDEX_DB_DIR = 'aitools/db'
AI_SOURCE_FILES = 'aitools/files'
AI_SOURCE_FILES_FULL = os.path.join(BASE_DIR, AI_SOURCE_FILES)
AI_DB_DIR = os.path.join(BASE_DIR, AI_INDEX_DB_DIR)
AI_MODEL_NAME = 'gpt-3.5-turbo'
# AI_MODEL_NAME = 'gpt-4'
AI_CHUNK_SIZE = 512
