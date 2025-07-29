def replace_and_save(original_file_path, new_file_path, old_word, new_word):
    """
    Replaces occurrences of a specific word in a file and saves the result to a new file.

    Args:
        original_file_path (str): The path to the original file.
        new_file_path (str): The path to the new file where modified content will be saved.
        old_word (str): The word to be replaced.
        new_word (str): The word to replace with.
    """
    try:
        with open(original_file_path, 'r') as infile:
            content = infile.read()

        modified_content = content.replace(old_word, new_word)

        with open(new_file_path, 'w') as outfile:
            outfile.write(modified_content)

        print(f"Successfully replaced '{old_word}' with '{new_word}' and saved to '{new_file_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{original_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Create a dummy original file for demonstration
with open("original.txt", "w") as f:
    f.write("This is an old text file.\nIt contains old information.\nLet's replace 'old' with 'new'.")

replace_and_save("original.txt", "new_file.txt", "old", "new")