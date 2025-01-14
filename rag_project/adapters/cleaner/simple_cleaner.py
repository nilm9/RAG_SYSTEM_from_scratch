# File: rag_project/adapters/cleaner/simple_cleaner.py

import re
from rag_project.core.ports.cleaner_port import CleanerPort

class SimpleCleaner(CleanerPort):
    """
    Adapter for basic text cleaning operations.
    """
    def clean(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text.strip()
