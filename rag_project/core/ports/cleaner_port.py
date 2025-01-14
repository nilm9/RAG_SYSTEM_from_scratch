from abc import ABC, abstractmethod

class CleanerPort(ABC):
    """
    Interface for text cleaning operations.
    """
    @abstractmethod
    def clean(self, text: str) -> str:
        """
        Clean text content from unwanted patterns.

        Args:
            text (str): The raw text content.

        Returns:
            str: Cleaned text.
        """
        pass
