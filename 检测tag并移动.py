import os
import shutil

def delete_image_by_tag(path, *args):
    files = os.listdir(path)
    image_extensions = ['.jpg', '.png', '.gif', '.bmp']
    deleted_path = os.path.join(path, "deleted_files")
    if not os.path.exists(deleted_path):
        os.mkdir(deleted_path)
    tagged_files = []
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.txt':
            full_path = os.path.join(path, file)
            with open(full_path, 'r') as f:
                content = f.read()
                for tag in args:
                    if tag in content:
                        tagged_files.append(name)
                        break
    
    for file in tagged_files:
        for ext in ['.txt'] + image_extensions:
            file_name = file + ext
            file_path = os.path.join(path, file_name)
            if os.path.exists(file_path):
                try:
                    shutil.move(file_path, deleted_path)
                    print(f"移动包含指定tag的文件：{file_path}")
                except Exception as e:
                    print(f"移动文件{file_path}时出现错误: {e}")



delete_image_by_tag(".","monochrome") 


#例子:delete_image_by_tag(".","greyscale","monochrome","no humans","6+girls","comic","text","dated","cover page","sample watermark")