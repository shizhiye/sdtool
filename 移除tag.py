import os

remove_tags = {'virtual youtuber', 'cowboy shot'}
txt_files = [f for f in os.listdir() if os.path.splitext(f)[1] == '.txt']
for txt_file in txt_files:
    file_path = os.path.join(os.getcwd(), txt_file)
    with open(file_path, 'r+') as f:
        tags = f.read().split(',')
        seen_tags = set() 
        new_tags = [] 
        for tag in tags:
            tag = tag.strip()
            if tag not in remove_tags and tag not in seen_tags: 
                new_tags.append(tag) 
                seen_tags.add(tag) 
        new_content = ','.join(new_tags)
        f.seek(0)
        f.write(new_content)
        f.truncate()
