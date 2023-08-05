import os
names = {}

for file in os.listdir('.'):  
    if file.endswith((".jpg",".png",".gif",".jpeg")):
        file_name,ext = os.path.splitext(file)
        names[file] = int(file_name.split("(")[1].split(")")[0])
        
  
for k in sorted(names.keys(), key=lambda x: names[x]):   
    i = names[k]   
    new_name = str(i) + ext   
    os.rename(k, new_name)