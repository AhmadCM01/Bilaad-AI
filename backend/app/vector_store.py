from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from backend.app.config import Config, IS_CONFIGURED
from langchain_community.vectorstores import SupabaseVectorStore

# Monkey-patch SupabaseVectorStore to pass all required parameters to match_documents
def patch_match_args(self, query, filter=None):
    ret = {
        "query_embedding": query,
        "match_threshold": 0.2,  # Similarity threshold
        "match_count": 5         # Maximum matches to return
    }
    if filter:
        ret["filter"] = filter
    return ret

SupabaseVectorStore.match_args = patch_match_args

# Initialize embeddings
embeddings = None
if Config.GEMINI_API_KEY:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=Config.GEMINI_API_KEY,
        output_dimensionality=768
    )

# Initialize vector store
vector_store = None

if IS_CONFIGURED and embeddings:
    try:
        from supabase.client import create_client
        from langchain_community.vectorstores import SupabaseVectorStore
        
        supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        vector_store = SupabaseVectorStore(
            client=supabase_client,
            embedding=embeddings,
            table_name="documents",
            query_name="match_documents"
        )
        print("[SUCCESS] Supabase pgvector store initialized successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Supabase vector store: {e}")
        print("[WARNING] Falling back to InMemoryVectorStore.")
        vector_store = InMemoryVectorStore(embeddings)
else:
    if embeddings:
        print("[INFO] Supabase not configured. Initializing InMemoryVectorStore with Gemini embeddings.")
        vector_store = InMemoryVectorStore(embeddings)
    else:
        print("[WARNING] Gemini API Key not found. Vector store and embeddings are disabled. Running in pure Mock mode.")
        vector_store = None

def get_vector_store():
    return vector_store
