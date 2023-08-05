import os

word = "v," # 你想要添加的词，后面加上一个逗号

folder = os.getcwd()

for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue
    filepath = os.path.join(folder, filename)
    with open(filepath, "r") as f:
        content = f.read()
    if word in content: # 检查是否已经添加了这个词
        continue
    else:
        f.close() # 关闭原来的文件
    new_content = f"{word}{content}" # 使用 f-string 拼接新内容
    with open(filepath, "w") as f:
        f.write(new_content)
    print(filename)
    print(new_content)
