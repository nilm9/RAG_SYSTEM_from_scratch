import os
import json


def notebooks_to_single_text(folder_path, output_file):
    """
    Reads all Jupyter (.ipynb) notebooks from folder_path,
    extracts the text from each cell, and appends it
    to output_file.
    """
    # Open the output file in write mode (will overwrite if it exists)
    with open(output_file, 'w', encoding='utf-8') as out_fp:

        # Loop over all files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file ends with .ipynb
            if filename.endswith('.ipynb'):
                notebook_path = os.path.join(folder_path, filename)

                # Read the notebook JSON
                with open(notebook_path, 'r', encoding='utf-8') as nb_fp:
                    notebook_data = json.load(nb_fp)

                # Write a header so you know which notebook this text comes from
                out_fp.write(f"===== Notebook: {filename} =====\n")

                # Each notebook has a list of cells under the "cells" key
                for cell in notebook_data.get("cells", []):
                    # cell["source"] is usually a list of strings representing each line
                    cell_lines = cell.get("source", [])
                    cell_text = "".join(cell_lines)

                    # Write the cell text to the output file, then a blank line
                    out_fp.write(cell_text)
                    out_fp.write("\n\n")


# Example usage:
if __name__ == "__main__":
    # Replace these paths with your own
    folder_path = "."
    output_file = "combined_notebooks.txt"

    notebooks_to_single_text(folder_path, output_file)
    print(f"All notebooks have been combined into '{output_file}'")
