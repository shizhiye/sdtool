import os
from wand.image import Image as WandImage
import skimage.color as color
import threading
import numpy as np
import hashlib
import concurrent.futures
import uuid
import shutil
import time
import logging

logger = logging.getLogger(__name__)

path = os.getcwd()
format = (".jpg", ".bmp", ".gif", ".jpeg", ".jfif")
save_format = ".png"     

def get_hash(filename):
    hashobj = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashobj.update(chunk)
    return hashobj.hexdigest()

def delete_duplicates(path):
    files = os.listdir(path) 
    hashes = set() 
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: 
        futures = [] 
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                full_path = os.path.join(path, file) 
                future = executor.submit(delete_file, full_path, hashes) 
                futures.append(future) 
        for future in concurrent.futures.as_completed(futures): 
            pass
    print("删除重复文件完成") 


def delete_file(full_path, hashes):
    try:
        file_hash = get_hash(full_path) 
        if file_hash in hashes: 
            print(f"删除重复文件: {full_path}")
            img = WandImage(filename=full_path) 
            img.close() 
            os.remove(full_path) 
        else: 
            hashes.add(file_hash)
    except Exception as e:
        print(f"处理文件{full_path}时出现错误: {e}") 
        
def convert_files(path):
    files = os.listdir(path)
    n = 8   
    m = len(files) // n
    threads = []
    for i in range(n):
        start = i * m
        end = start + m
        if i == n - 1:
            end = len(files)
        t = threading.Thread(target=convert, args=(files[start:end],))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("转换图片格式完成") 
    

def convert(files):
    for file in files:
        if file.lower().endswith(tuple(format)):
            file_name, extension = os.path.splitext(file)
            try:
                with WandImage(filename=file) as img:    
                    try:
                        img.save(filename=file_name + save_format)    
                        time.sleep(0.5)  
                        print(f"转换图片格式: {file} -> {file_name + save_format}")    
                    except OSError:
                        new_name = file_name + "_bad" + extension
                        os.rename(file, new_name)
                        shutil.move(new_name, os.path.join("bad_images", new_name))
                        print(f"移动有问题的图片: {new_name}")
            except IOError as e:
                logger.error(f"无法打开图片: {file}")
                new_name = file_name + "_bad" + extension
                os.rename(file, new_name)
                shutil.move(new_name, os.path.join("bad_images", new_name))
                print(f"移动有问题的图片: {new_name}") 
            except ValueError as e:
                logger.error(f"图片 '{file}' 出现异常: {e}")
                new_name = file_name + "_bad" + extension
                os.rename(file, new_name)
                shutil.move(new_name, os.path.join("bad_images", new_name))
                print(f"移动有问题的图片: {new_name}")               
            os.remove(file)
            
    
def check_image_integrity(path):
    try:
        img = WandImage(filename=path)
        img.flip()
        print(f'图片完整: {path}')
        img.close()
        return True, path 
    except Exception as e:
        print(f'图片不完整: {path}')
        print(e)
        return False, path 


def check_all_images(root):
    filenames = os.listdir(root)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if filename.lower().endswith(('.jpg', '.png', '.gif')):
                future = executor.submit(check_image_integrity, filepath)
                futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            result,path = future.result()
            if not result:
                os.makedirs("deleted_files", exist_ok=True)  
                shutil.move(path, os.path.join("deleted_files", os.path.basename(path)))
                print(f'移动不完整的图片: {path}')
                
delete_duplicates(path)
files = os.listdir(path)
convert_files(path)
check_all_images('.')

print("处理完成！")