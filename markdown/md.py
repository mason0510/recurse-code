import os

def extract_md_content(path):
    content = ""
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def process_directory(root_dir, output_file):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)
                content = extract_md_content(file_path)
                output_file.write(content + '\n')

def main():
    root_dir = '/Users/houzi/home/Javacode/demo/recurse-code'  # 请将此路径替换为您的实际仓库路径
    output_file_path = 'output.txt'

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        process_directory(root_dir, output_file)
    print("文本内容已合并到：", output_file_path)

if __name__ == '__main__':
    main()
