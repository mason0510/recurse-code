import os

def display_directory_tree(root_dir, output_file, prefix=""):
    files = os.listdir(root_dir)
    entries = [os.path.join(root_dir, entry) for entry in files]
    entries.sort(key=lambda x: (os.path.isdir(x), x))

    for index, entry in enumerate(entries):
        if os.path.basename(entry) == "vendor":
            continue

        is_last = index == len(entries) - 1
        if os.path.isdir(entry):
            marker = "└── " if is_last else "├── "
            output_file.write(prefix + marker + os.path.basename(entry) + "\n")
            new_prefix = "    " if is_last else "│   "
            display_directory_tree(entry, output_file, prefix + new_prefix)
        else:
            marker = "└── " if is_last else "├── "
            output_file.write(prefix + marker + os.path.basename(entry) + "\n")

def main():
    project_path = "path/to/your/go/project"  # 请将此路径替换为您的实际Go项目路径

    with open("directory_structure.txt", "w", encoding="utf-8") as output_file:
        display_directory_tree(project_path, output_file)

    print("目录结构已保存到：directory_structure.txt")

if __name__ == "__main__":
    main()
