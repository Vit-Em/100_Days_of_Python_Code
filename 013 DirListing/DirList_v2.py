import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import humanize

def get_directory(title):
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=title)
    return folder_selected

def get_save_path(initial_filename):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialfile=initial_filename
    )
    return file_path

def get_size_and_modified(path):
    stats = os.stat(path)
    size = humanize.naturalsize(stats.st_size)
    modified = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    return size, modified

def generate_tree(startpath):
    tree = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        size, modified = get_size_and_modified(root)
        tree.append(f'{modified}\t{indent}{os.path.basename(root)}/\t{size}')
        subindent = '│   ' * level + '├── '
        for f in files:
            filepath = os.path.join(root, f)
            size, modified = get_size_and_modified(filepath)
            tree.append(f'{modified}\t{subindent}{f}\t{size}')
    return '\n'.join(tree)

def save_tree(tree, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(tree)
    print(f"Tree saved to {save_path}")

def main():
    directory = get_directory("Select the root directory for analysis")
    if directory:
        tree = generate_tree(directory)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        root_name = os.path.basename(directory)
        initial_filename = f"{timestamp}_{root_name}.txt"
        save_path = get_save_path(initial_filename)
        if save_path:
            save_tree(tree, save_path)
        else:
            print("Save operation cancelled.")
    else:
        print("No directory selected.")

if __name__ == "__main__":
    main()
