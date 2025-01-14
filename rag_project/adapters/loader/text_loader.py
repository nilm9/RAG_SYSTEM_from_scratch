import os
from rag_project.core.domain.document import Document
from rag_project.core.ports.plugin_port import Plugin


class TextLoader(Plugin):
    """
    Adapter for loading text files.
    """
    def supports(self, filename: str) -> bool:
        return filename.endswith('.txt')

    def load(self, filepath: str) -> Document:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return Document(filename=os.path.basename(filepath), content=content)
