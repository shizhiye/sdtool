import os
import shutil
import re
import random
import numpy as np
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity 

def delete_similar_images_by_tag(path, threshold=0.8):
    image_extensions = {'.jpg', '.png', '.gif', '.bmp'}
    deleted_path = os.path.join(path, 'deleted_files')
    if not os.path.exists(deleted_path):
        os.mkdir(deleted_path)

    def extract_tags(txt_path):
        with open(txt_path, 'r', encoding='shift-jis') as f:
            content = f.read()
            return set(re.findall(r'\b\w+\b', content))

    def get_image_tags(image_path):
        image_name = os.path.basename(image_path)
        if image_name not in tag_dict:
            txt_name = os.path.splitext(image_name)[0] + '.txt'
            txt_path = os.path.join(os.path.dirname(image_path), txt_name)
            if os.path.exists(txt_path):
                tag_dict[image_name] = extract_tags(txt_path)
        return tag_dict.get(image_name, set())

    def delete_image(image_path):
        image_name = os.path.basename(image_path)
        deleted_image_path = os.path.join(deleted_path, image_name)
        if os.path.exists(image_path):
            shutil.move(image_path, deleted_image_path)
            image_list.remove(image_path)
            deleted_set.add(image_path)
            tag_dict.pop(image_name, None)
        else:
            print(f"文件不存在: {image_path}")

    def process_images():
        if not image_list: 
            return
        image_list_copy = image_list.copy()
        for i in range(len(image_list_copy)):
            image_path = image_list_copy[i]
            tags1 = get_image_tags(image_path)
            if not tags1:
                continue
            for j in range(i + 1, len(image_list_copy)):
                other_path = image_list_copy[j]
                if other_path in deleted_set:
                    continue
                tags2 = get_image_tags(other_path)
                if not tags2:
                    continue
                all_tags = list(tags1.union(tags2))
                vec1 = np.array([int(tag in tags1) for tag in all_tags])
                vec2 = np.array([int(tag in tags2) for tag in all_tags])
                similarity = cosine_similarity(vec1.reshape(1,-1), vec2.reshape(1,-1))[0][0]
                if similarity >= threshold:
                    if not os.path.exists(image_path) or not os.path.exists(other_path):
                        continue
                    size1 = os.path.getsize(image_path)
                    size2 = os.path.getsize(other_path)
                    if size1 == size2:
                        image_to_delete = random.choice([image_path, other_path])
                    else:
                        image_to_delete = image_path if size1 < size2 else other_path
                    print(f"相似度: {os.path.basename(image_path)} 和 {os.path.basename(other_path)} 是 {similarity:.2f},删除相似的图片: {image_to_delete}")
                    delete_image(image_to_delete)

    tag_dict = {}
    image_list = []
    deleted_set = set()

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1] in image_extensions:
                image_path = os.path.join(dirpath, filename)
                image_list.append(image_path)

    while True:
        count = len(tag_dict)
        process_images()
        if count == len(tag_dict):
            break

    print('删除完成')

path = '.'
threshold = 0.95 #相似度在这里0-1
delete_similar_images_by_tag(path, threshold)
