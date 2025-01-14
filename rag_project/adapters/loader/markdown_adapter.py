
import markdown

def convert_markdown_to_text(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
        return markdown.markdown(md_content)
