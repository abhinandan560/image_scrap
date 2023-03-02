import os

import requests
from bs4 import BeautifulSoup
from pymongo

save_dir="images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# fake user agent to avoid getting blocked by Google
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

querystring="abhinandan patil"

response=requests.get(f"https://www.google.com/search?q={querystring}&tbm=isch&ved=2ahUKEwjxjL2y5b39AhUT1zgGHd7GDc8Q2-cCegQIABAA&oq=abhinandan+patil&gs_lcp=CgNpbWcQARgAMgUIABCABDIGCAAQBRAeMgcIABCABBAYMgcIABCABBAYOgcIABCxAxBDOgwIABANEIAEELEDEBM6DwgAEA0QgAQQsQMQgwEQEzoJCAAQDRCABBATOggIABCABBCxAzoLCAAQgAQQsQMQgwE6BAgAEENQhAhYixJg8B1oAHAAeACAAbEDiAHJCZIBCTAuNS4xLjAuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=wt8AZPGjJZOu4-EP3o23-Aw&rlz=1C1GCEU_enIN975IN975&safe=active",verify=False)

soup=BeautifulSoup(response.content,'html.parser')

images_tag=soup.find_all('img')

del images_tag[0]

image_scrap_list=[]
for i in images_tag:
    image_url=i['src']

    image_data=requests.get(image_url,verify=False).content
    image_dict={"image_url":image_url,"image_data":image_data}
    image_scrap_list.append(image_dict)

    with open(os.path.join(save_dir, f"{querystring}_{images_tag.index(i)}.jpg"),"wb") as f:
        f.write(image_data)

client=pymongo.MongoClient("mongodb+srv://abhinandan:admin@cluster0.mwmc8cj.mongodb.net/?retryWrites=true&w=majority")
db=client["image_scrap"]
image_coll=db["image_coll"]
image_coll.insert_many(image_scrap_list)



