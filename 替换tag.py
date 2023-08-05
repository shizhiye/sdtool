import os

remove_tags = ['hand up',] 
replace_tags = ['hand on own chin',] 
txt_files = [f for f in os.listdir() if os.path.splitext(f)[1] == '.txt']
for txt_file in txt_files:
    file_path = os.path.join(os.getcwd(), txt_file)
    with open(file_path, 'r+') as f:
        tags = f.read().split(',')
        seen_tags = set() 
        new_tags = [] 
        for i, tag in enumerate(tags):
            tag = tag.strip()
            if tag in remove_tags: 
                new_tag = replace_tags[remove_tags.index(tag)]
                if new_tag not in seen_tags:
                    new_tags.append(new_tag) 
                    seen_tags.add(new_tag) 
            elif tag not in seen_tags: 
                new_tags.append(tag) 
                seen_tags.add(tag) 
        new_content = ','.join(new_tags)
        f.seek(0)
        f.write(new_content)
        f.truncate()
