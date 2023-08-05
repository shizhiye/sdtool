import os
import requests
from bs4 import BeautifulSoup
import time 
import random 
import tqdm 

base_url = 'https://yande.re/post?tags=123&page=' #定义tag,tags=123

page_num = 1 #抓取多少页

page_urls = [f"{base_url}{page}" for page in range(1, page_num + 1)]
print(f"页面链接总数：{len(page_urls)}")
os.makedirs('images', exist_ok=True) 
start_time = time.time()

img_urls = []
for i, url in tqdm.tqdm(enumerate(page_urls), desc="正在下载页面链接", unit="页", leave=False):
    try:
        response = requests.get(url, timeout=60) 
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('a', class_='directlink largeimg') 
        img_urls.extend([img['href'] for img in img_tags])
    except (requests.Timeout, requests.ConnectionError) as e:
        tqdm.tqdm.write(f"发生错误: {e}，等待30秒后重试")
        time.sleep(30)
        continue
        
print(f"页面链接总数：{len(page_urls)}")
print(f"图片链接总数：{len(img_urls)}")

random.shuffle(img_urls)
success_count = 0
for j, url in tqdm.tqdm(enumerate(img_urls), desc="正在下载图片", unit="张", leave=False):
    filepath = os.path.join('images', os.path.basename(url))
    if os.path.exists(filepath):
        tqdm.tqdm.write(f"该图片已经存在于本地：{filepath}")
        continue
    try:
        response = requests.get(url, timeout=10) 
        if response.status_code == 200:
            open(filepath, 'wb').write(response.content)
            success_count += 1
            sleep_time = random.randint(1, 1) #每个图片的延迟
            tqdm.tqdm.write(f"成功下载第{success_count}张图片，睡眠时间: {sleep_time}秒")
            time.sleep(sleep_time)
        else: 
            tqdm.tqdm.write(f"下载失败，状态码: {response.status_code}")
    except Exception as e:
        tqdm.tqdm.write(f"下载失败，错误信息: {e}")

print("图片下载完成！")