#!/usr/bin/env python3
"""
Vector Database Integration for M.I.A. Consciousness Research System
Supports ChromaDB, FAISS, and Pinecone for semantic search and embeddings
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
import asyncio
from dataclasses import dataclass

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class VectorSearchResult:
    """Result from vector search"""
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    embedding: Optional[np.ndarray] = None

@dataclass
class VectorConfig:
    """Configuration for vector database"""
    backend: str = "chromadb"  # chromadb, faiss, pinecone
    model_name: str = "all-MiniLM-L6-v2"
    dimension: int = 384
    collection_name: str = "mia_consciousness"
    persist_directory: str = "./vector_db"
    
    # Pinecone specific
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    
    # FAISS specific
    faiss_index_type: str = "IndexFlatIP"  # IndexFlatIP, IndexIVFFlat, etc.
    
    # ChromaDB specific
    chromadb_host: str = "localhost"
    chromadb_port: int = 8000

class EmbeddingGenerator:
    """Generate embeddings using various models"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers not available")
        
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise
    
    def encode(self, texts: Union[str, List[str]], 
               normalize: bool = True) -> np.ndarray:
        """Generate embeddings for texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(texts, normalize_embeddings=normalize)
        return embeddings
    
    def encode_batch(self, texts: List[str], 
                    batch_size: int = 32,
                    normalize: bool = True) -> np.ndarray:
        """Generate embeddings in batches"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.encode(batch, normalize=normalize)
            all_embeddings.append(embeddings)
        
        return np.vstack(all_embeddings)

class ChromaDBBackend:
    """ChromaDB vector database backend"""
    
    def __init__(self, config: VectorConfig):
        if not CHROMADB_AVAILABLE:
            raise ImportError("chromadb not available")
        
        self.config = config
        self.client = None
        self.collection = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent client
            self.client = chromadb.PersistentClient(
                path=self.config.persist_directory
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.config.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB initialized: {self.config.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents(self, documents: List[str], 
                     metadatas: List[Dict[str, Any]],
                     ids: List[str],
                     embeddings: Optional[List[List[float]]] = None):
        """Add documents to the collection"""
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def search(self, query_embeddings: List[List[float]], 
              n_results: int = 10) -> List[VectorSearchResult]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
            
            search_results = []
            for i in range(len(results['ids'][0])):
                result = VectorSearchResult(
                    id=results['ids'][0][i],
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i],
                    score=1 - results['distances'][0][i]  # Convert distance to similarity
                )
                search_results.append(result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(self.config.collection_name)
            logger.info(f"Deleted collection: {self.config.collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")

class FAISSBackend:
    """FAISS vector database backend"""
    
    def __init__(self, config: VectorConfig):
        if not FAISS_AVAILABLE:
            raise ImportError("faiss not available")
        
        self.config = config
        self.index = None
        self.documents = []
        self.metadatas = []
        self.ids = []
        self._initialize()
    
    def _initialize(self):
        """Initialize FAISS index"""
        try:
            if self.config.faiss_index_type == "IndexFlatIP":
                self.index = faiss.IndexFlatIP(self.config.dimension)
            elif self.config.faiss_index_type == "IndexFlatL2":
                self.index = faiss.IndexFlatL2(self.config.dimension)
            else:
                raise ValueError(f"Unsupported index type: {self.config.faiss_index_type}")
            
            logger.info(f"FAISS index initialized: {self.config.faiss_index_type}")
            
        except Exception as e:
            logger.error(f"Failed to initialize FAISS: {e}")
            raise
    
    def add_documents(self, documents: List[str], 
                     metadatas: List[Dict[str, Any]],
                     ids: List[str],
                     embeddings: List[List[float]]):
        """Add documents to the index"""
        try:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            self.index.add(embeddings_array)
            
            self.documents.extend(documents)
            self.metadatas.extend(metadatas)
            self.ids.extend(ids)
            
            logger.info(f"Added {len(documents)} documents to FAISS")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def search(self, query_embeddings: List[List[float]], 
              n_results: int = 10) -> List[VectorSearchResult]:
        """Search for similar documents"""
        try:
            query_array = np.array(query_embeddings, dtype=np.float32)
            scores, indices = self.index.search(query_array, n_results)
            
            search_results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    result = VectorSearchResult(
                        id=self.ids[idx],
                        content=self.documents[idx],
                        metadata=self.metadatas[idx],
                        score=float(scores[0][i])
                    )
                    search_results.append(result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def save_index(self, filepath: str):
        """Save FAISS index to file"""
        try:
            faiss.write_index(self.index, filepath)
            
            # Save metadata
            metadata_file = filepath.replace('.index', '_metadata.json')
            metadata = {
                'documents': self.documents,
                'metadatas': self.metadatas,
                'ids': self.ids
            }
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f)
            
            logger.info(f"FAISS index saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
    def load_index(self, filepath: str):
        """Load FAISS index from file"""
        try:
            self.index = faiss.read_index(filepath)
            
            # Load metadata
            metadata_file = filepath.replace('.index', '_metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self.documents = metadata['documents']
                    self.metadatas = metadata['metadatas']
                    self.ids = metadata['ids']
            
            logger.info(f"FAISS index loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")

class VectorDatabase:
    """Main vector database interface"""
    
    def __init__(self, config: VectorConfig):
        self.config = config
        self.embedding_generator = EmbeddingGenerator(config.model_name)
        self.backend = None
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Initialize the selected backend"""
        if self.config.backend == "chromadb":
            self.backend = ChromaDBBackend(self.config)
        elif self.config.backend == "faiss":
            self.backend = FAISSBackend(self.config)
        elif self.config.backend == "pinecone":
            # TODO: Implement Pinecone backend
            raise NotImplementedError("Pinecone backend not yet implemented")
        else:
            raise ValueError(f"Unsupported backend: {self.config.backend}")
    
    def add_documents(self, documents: List[str], 
                     metadatas: Optional[List[Dict[str, Any]]] = None,
                     ids: Optional[List[str]] = None,
                     generate_embeddings: bool = True) -> bool:
        """Add documents to the vector database"""
        try:
            # Generate IDs if not provided
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Generate metadata if not provided
            if metadatas is None:
                metadatas = [{"source": "unknown"} for _ in documents]
            
            # Generate embeddings if requested
            embeddings = None
            if generate_embeddings:
                embeddings = self.embedding_generator.encode(documents)
                embeddings = embeddings.tolist()
            
            # Add to backend
            self.backend.add_documents(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def search(self, query: str, 
              n_results: int = 10) -> List[VectorSearchResult]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.encode([query])
            query_embedding = query_embedding.tolist()
            
            # Search using backend
            results = self.backend.search(query_embedding, n_results)
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def search_with_filter(self, query: str,
                          metadata_filter: Dict[str, Any],
                          n_results: int = 10) -> List[VectorSearchResult]:
        """Search with metadata filtering (ChromaDB only for now)"""
        if self.config.backend != "chromadb":
            logger.warning("Metadata filtering only supported with ChromaDB")
            return self.search(query, n_results)
        
        try:
            query_embedding = self.embedding_generator.encode([query])
            query_embedding = query_embedding.tolist()
            
            results = self.backend.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                where=metadata_filter
            )
            
            search_results = []
            for i in range(len(results['ids'][0])):
                result = VectorSearchResult(
                    id=results['ids'][0][i],
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i],
                    score=1 - results['distances'][0][i]
                )
                search_results.append(result)
            
            return search_results
            
        except Exception as e:
            logger.error(f"Filtered search failed: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            if self.config.backend == "chromadb":
                count = self.backend.collection.count()
                return {
                    "backend": self.config.backend,
                    "collection_name": self.config.collection_name,
                    "document_count": count,
                    "model_name": self.config.model_name
                }
            elif self.config.backend == "faiss":
                return {
                    "backend": self.config.backend,
                    "document_count": len(self.backend.documents),
                    "index_size": self.backend.index.ntotal,
                    "model_name": self.config.model_name
                }
            else:
                return {"backend": self.config.backend}
                
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}

# Utility functions
def create_vector_database(backend: str = "chromadb",
                          model_name: str = "all-MiniLM-L6-v2",
                          collection_name: str = "mia_consciousness") -> VectorDatabase:
    """Create a vector database with default configuration"""
    config = VectorConfig(
        backend=backend,
        model_name=model_name,
        collection_name=collection_name
    )
    return VectorDatabase(config)

def chunk_text(text: str, chunk_size: int = 500, 
               overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        if end >= len(text):
            break
            
        start = end - overlap
    
    return chunks

async def process_documents_async(vector_db: VectorDatabase,
                                documents: List[str],
                                batch_size: int = 100) -> bool:
    """Process documents asynchronously in batches"""
    try:
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            success = vector_db.add_documents(batch)
            
            if not success:
                logger.error(f"Failed to process batch {i//batch_size + 1}")
                return False
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.1)
        
        return True
        
    except Exception as e:
        logger.error(f"Async processing failed: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create vector database
    vector_db = create_vector_database()
    
    # Add some test documents
    documents = [
        "Consciousness is the state of being aware of and able to think about one's existence.",
        "Neural correlates of consciousness are the minimal neural mechanisms sufficient for consciousness.",
        "The hard problem of consciousness refers to the difficulty of explaining subjective experience.",
        "Integrated Information Theory proposes that consciousness corresponds to integrated information."
    ]
    
    metadatas = [
        {"topic": "consciousness", "type": "definition"},
        {"topic": "neuroscience", "type": "concept"},
        {"topic": "philosophy", "type": "problem"},
        {"topic": "theory", "type": "hypothesis"}
    ]
    
    # Add documents
    success = vector_db.add_documents(documents, metadatas)
    print(f"Documents added: {success}")
    
    # Search
    results = vector_db.search("What is consciousness?", n_results=3)
    print(f"\nSearch results for 'What is consciousness?':")
    for result in results:
        print(f"Score: {result.score:.3f} - {result.content[:100]}...")
    
    # Get stats
    stats = vector_db.get_collection_stats()
    print(f"\nCollection stats: {stats}")