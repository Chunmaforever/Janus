import math
import re
from typing import List, Dict, Set

class TFIDFSimilarity:
    """
    A lightweight TF-IDF cosine similarity engine without external dependencies.
    """
    
    def __init__(self):
        self.stop_words = {"the", "and", "a", "of", "to", "in", "is", "for", "with", "that", "this", "on", "as", "an"}

    def _tokenize(self, text: str) -> List[str]:
        """Lowercases and splits text into tokens, removing stop words."""
        tokens = re.findall(r'\w+', text.lower())
        return [t for t in tokens if t not in self.stop_words and len(t) > 2]

    def _get_tf(self, tokens: List[str]) -> Dict[str, float]:
        """Calculates Term Frequency (normalized)."""
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        
        total = len(tokens)
        if total == 0:
            return {}
            
        return {k: v / total for k, v in tf.items()}

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculates cosine similarity between two word-frequency dictionaries."""
        all_keys = set(vec1.keys()) | set(vec2.keys())
        
        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0
        
        for key in all_keys:
            v1 = vec1.get(key, 0.0)
            v2 = vec2.get(key, 0.0)
            dot_product += v1 * v2
            norm1 += v1 ** 2
            norm2 += v2 ** 2
            
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))

    def score(self, query: str, document: str) -> float:
        """
        Calculates the similarity score between a query and a document.
        Uses simple TF (normalized) and cosine similarity as a simplified similarity metric.
        """
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(document)
        
        if not query_tokens or not doc_tokens:
            return 0.0
            
        query_tf = self._get_tf(query_tokens)
        doc_tf = self._get_tf(doc_tokens)
        
        return self._cosine_similarity(query_tf, doc_tf)
