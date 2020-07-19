from flask import Flask
from bs4 import BeautifulSoup as BS
import requests
import json
import urllib



app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return get_result("telephones"," ")
    

@app.route('/scrap/<cat>/<keyword>', methods=['GET', 'POST'])
def scrap(cat,keyword):
    return get_result(cat,keyword)

def get_result(cat,keyword,page_count=5):
    adsSer =[]
    adSerIds = []
    for index in range(1,page_count) :
        print("In page "+str(index))
        print("In cat "+str(cat))
        print("with keyword "+str(keyword))
        print("----------------------------------")
        base_url = "https://www.ouedkniss.com/annonces/index.php?c="+cat+"&keywords="+str(keyword)+"&p="+str(index)
        page = requests.get(base_url)
        bs = BS(page.text)
        content = bs.find_all('div', {'id':'resultat'})
        
        if len(content)>0:
            ads = content[0].find_all('div', {'class':['annonce annonce_store','annonce']})
            for ad in ads:
                adSer = {}
                title = ad.find('h2', {'itemprop':'name'})
                desc = ad.find('span', {'class':'annonce_description_preview'})
                if title != None :
                    if keyword.lower() in title.contents[0].lower() or desc != None and len(desc.contents)>=1 and keyword.lower() in desc.contents[0].lower():
                        adSer["title"]=title.contents[0]
                        print(adSer["title"])
                        if ad.find("a") != None :
                            link = ad.find("a").get('href')
                            desc_tech = ad.find('span', {'class':'annonce_get_description'})
                            desc = ad.find('span', {'class':'annonce_description_preview'})
                            city = ad.find('span', {'class':'titre_wilaya'})
                            #image = ad.find('img', {'itemprop':'image'}).get("data-src")
                            price = ad.find('span', {'itemprop':'price'})
                            id = ad.find('span', {'class':'annonce_numero'})
                            if link != None :
                                adSer["link"]="https://www.ouedkniss.com/"+link
                            if desc != None and len(desc.contents)>=1:
                                adSer["desc"]=desc.contents[0]
                            if city != None and len(city.contents)>=1:
                                adSer["city"]=city.contents[0]
                            if price != None and len(price.contents)>=1:
                                adSer["price"]=price.contents[0]
                            if id != None and len(id.contents)>=1:
                                adSer["id"]=id.contents[0]
                            
                            adSer["image"]="https://img1.ouedkniss.com/photos_annonces/"+adSer["id"]+"/Min_large.jpg"
                            if adSer["id"] not in adSerIds :
                                adSerIds.append(adSer["id"])
                                adsSer.append(adSer)
    print(adSerIds)
    return json.dumps(adsSer, ensure_ascii=True),200
    





