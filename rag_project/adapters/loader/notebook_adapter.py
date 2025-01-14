import os
import json
from rag_project.core.domain.document import Document
from rag_project.core.ports.plugin_port import Plugin


class NotebookLoader(Plugin):
    """
    Adapter for loading Jupyter Notebook files.
    """
    def supports(self, filename: str) -> bool:
        return filename.endswith('.ipynb')

    def load(self, filepath: str) -> Document:
        with open(filepath, 'r', encoding='utf-8') as file:
            notebook = json.load(file)
        extracted_content = []
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "markdown":
                extracted_content.append("".join(cell.get("source", [])))
        return Document(filename=os.path.basename(filepath), content="\n".join(extracted_content))
