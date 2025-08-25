from sentence_transformers import SentenceTransformer
import hdbscan
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Any
import re
from bertopic import BERTopic
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class SemanticSegmentation:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Initialize models
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
    def segment_topics(self, extracted_text: str) -> Dict[str, Any]:
        """
        Task 2: Semantic Segmentation & Topic Detection
        Split text into digestible topics and label them automatically
        """
        try:
            # Step 1: Preprocess and chunk text
            chunks = self._create_text_chunks(extracted_text)
            
            if len(chunks) < 2:
                # If not enough chunks, create artificial segmentation
                chunks = self._create_artificial_chunks(extracted_text)
            
            # Step 2: Generate embeddings
            embeddings = self.embedding_model.encode(chunks)
            
            # Step 3: Cluster chunks using HDBSCAN
            clusters = self._cluster_chunks(embeddings, chunks)
            
            # Step 4: Generate topic labels
            topics = self._generate_topic_labels(clusters, chunks)
            
            # Step 5: Calculate confidence scores
            topics_with_confidence = self._calculate_topic_confidence(topics, embeddings)
            
            return {
                "topics": topics_with_confidence,
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            raise Exception(f"Topic segmentation failed: {str(e)}")
    
    def _create_text_chunks(self, text: str) -> List[str]:
        """Create meaningful text chunks from the input text"""
        # Split into sentences first
        sentences = sent_tokenize(text)
        
        chunks = []
        current_chunk = ""
        target_chunk_size = 200  # Target words per chunk
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            if len(current_chunk.split()) + sentence_words <= target_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Filter out very short chunks
        chunks = [chunk for chunk in chunks if len(chunk.split()) >= 10]
        
        return chunks
    
    def _create_artificial_chunks(self, text: str) -> List[str]:
        """Create artificial chunks when natural segmentation fails"""
        # Split by paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) >= 2:
            return paragraphs
        
        # Split by sentences
        sentences = sent_tokenize(text)
        
        # Group sentences into chunks
        chunks = []
        current_chunk = ""
        sentences_per_chunk = 3
        
        for i, sentence in enumerate(sentences):
            current_chunk += " " + sentence if current_chunk else sentence
            
            if (i + 1) % sentences_per_chunk == 0:
                chunks.append(current_chunk.strip())
                current_chunk = ""
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [text[:500], text[500:1000]] if len(text) > 500 else [text]
    
    def _cluster_chunks(self, embeddings: np.ndarray, chunks: List[str]) -> Dict[int, List[int]]:
        """Cluster text chunks using HDBSCAN"""
        # Determine optimal parameters based on data size
        n_samples = len(embeddings)
        
        if n_samples < 5:
            # For very small datasets, create simple clusters
            return {0: list(range(n_samples))}
        
        # HDBSCAN parameters
        min_cluster_size = max(2, n_samples // 10)
        min_samples = max(1, min_cluster_size // 2)
        
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        
        cluster_labels = clusterer.fit_predict(embeddings)
        
        # Group chunks by cluster
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
        
        return clusters
    
    def _generate_topic_labels(self, clusters: Dict[int, List[int]], chunks: List[str]) -> List[Dict[str, Any]]:
        """Generate topic labels for each cluster"""
        topics = []
        
        for cluster_id, chunk_indices in clusters.items():
            if cluster_id == -1:  # Noise points
                continue
            
            # Get chunks for this cluster
            cluster_chunks = [chunks[i] for i in chunk_indices]
            
            # Generate topic name
            topic_name = self._extract_topic_name(cluster_chunks)
            
            # Create topic chunks with metadata
            topic_chunks = []
            for i, chunk in enumerate(cluster_chunks):
                topic_chunks.append({
                    "id": chunk_indices[i],
                    "text": chunk,
                    "confidence": self._calculate_chunk_confidence(chunk)
                })
            
            topics.append({
                "topic_name": topic_name,
                "chunks": topic_chunks,
                "confidence_score": 0.0  # Will be calculated later
            })
        
        return topics
    
    def _extract_topic_name(self, chunks: List[str]) -> str:
        """Extract a meaningful topic name from cluster chunks"""
        # Combine all chunks
        combined_text = " ".join(chunks)
        
        # Extract potential topic names using TF-IDF
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([combined_text])
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get top terms
            tfidf_scores = tfidf_matrix.toarray()[0]
            top_indices = np.argsort(tfidf_scores)[-5:]  # Top 5 terms
            
            top_terms = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]
            
            if top_terms:
                # Create a topic name from top terms
                topic_name = " ".join(top_terms[:3]).title()
                return topic_name
        
        except Exception:
            pass
        
        # Fallback: extract from first sentence
        first_chunk = chunks[0] if chunks else ""
        sentences = sent_tokenize(first_chunk)
        
        if sentences:
            first_sentence = sentences[0]
            # Extract first few meaningful words
            words = first_sentence.split()[:5]
            topic_name = " ".join(words).title()
            return topic_name
        
        return "General Topic"
    
    def _calculate_chunk_confidence(self, chunk: str) -> float:
        """Calculate confidence score for a text chunk"""
        if not chunk:
            return 0.0
        
        # Factors affecting confidence:
        # 1. Length (optimal length is better)
        # 2. Completeness (ends with proper punctuation)
        # 3. Vocabulary richness
        
        length_score = min(1.0, len(chunk.split()) / 50)  # Optimal around 50 words
        
        completeness_score = 1.0 if chunk.strip().endswith(('.', '!', '?')) else 0.7
        
        # Vocabulary richness (unique words / total words)
        words = chunk.lower().split()
        if words:
            unique_words = len(set(words))
            richness_score = unique_words / len(words)
        else:
            richness_score = 0.0
        
        # Weighted average
        confidence = (length_score * 0.4 + completeness_score * 0.3 + richness_score * 0.3)
        return round(confidence, 2)
    
    def _calculate_topic_confidence(self, topics: List[Dict[str, Any]], embeddings: np.ndarray) -> List[Dict[str, Any]]:
        """Calculate confidence scores for topics based on cluster quality"""
        for topic in topics:
            chunk_confidences = [chunk["confidence"] for chunk in topic["chunks"]]
            
            if chunk_confidences:
                # Average confidence of chunks in the topic
                avg_confidence = sum(chunk_confidences) / len(chunk_confidences)
                
                # Boost confidence based on topic size (more chunks = more confident)
                size_boost = min(0.2, len(topic["chunks"]) * 0.05)
                
                topic["confidence_score"] = round(min(1.0, avg_confidence + size_boost), 2)
            else:
                topic["confidence_score"] = 0.0
        
        return topics
