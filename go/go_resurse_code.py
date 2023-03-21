# import os
# import shutil
#
# def copy_go_file_with_comment(src_path, dest_path):
#     with open(src_path, "r", encoding="utf-8") as src_file:
#         content = src_file.read()
#
#     with open(dest_path, "w", encoding="utf-8") as dest_file:
#         dest_file.write(f"<!-- {os.path.relpath(src_path)} -->\n")
#         dest_file.write("```go\n")
#         dest_file.write(content)
#         dest_file.write("\n```\n\n")
#
# def process_directory(root_dir, output_dir):
#     for subdir, dirs, files in os.walk(root_dir):
#         for file in files:
#             if file.endswith('.go'):
#                 file_path = os.path.join(subdir, file)
#                 relative_path = os.path.relpath(file_path, root_dir)
#                 dest_path = os.path.join(output_dir, relative_path + ".md")
#                 os.makedirs(os.path.dirname(dest_path), exist_ok=True)
#                 copy_go_file_with_comment(file_path, dest_path)
#
# def main():
#     root_dir = '/Users/houzi/home/pandaCapital/chat/alchemyapi-go'  # 请将此路径替换为您的实际仓库路径
#     output_dir = 'go_files'
#
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     process_directory(root_dir, output_dir)
#     print("Go文件已复制到：", output_dir)
#
# if __name__ == '__main__':
#     main()

import os

def append_go_file_with_comment(src_path, dest_file):
    with open(src_path, "r", encoding="utf-8") as src_file:
        content = src_file.read()

    dest_file.write(f"<!-- {os.path.relpath(src_path)} -->\n")
    dest_file.write("```go\n")
    dest_file.write(content)
    dest_file.write("\n```\n\n")

def process_directory(root_dir, output_file):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.go'):
                file_path = os.path.join(subdir, file)
                append_go_file_with_comment(file_path, output_file)

def main():
    root_dir = '/Users/houzi/home/pandaCapital/chat/alchemyapi-go'  # 请将此路径替换为您的实际仓库路径
    output_filename = 'merged_go_files.md'

    with open(output_filename, "w", encoding="utf-8") as output_file:
        process_directory(root_dir, output_file)

    print("Go文件已合并到：", output_filename)

if __name__ == '__main__':
    main()
