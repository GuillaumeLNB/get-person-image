import requests
import urllib.parse
from requests import Session

# most used User-Agent
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'

def get_image_url(pax_name:str)->str:
    "return the image url based on the person name"
    with Session() as s:
        # getting the list of the Qid
        r = s.get('https://www.wikidata.org/w/api.php?action=wbsearchentities&search='+pax_name+'&language=fr&origin=*&format=json')
        if not r.ok:
            return
        q_id = r.json()['search'][0]['id']
        # fetching the list of pictures
        r2 = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&origin=*&format=json&ids="+q_id)
        if not r.ok:
            return
        image_url = r2.json()['entities'][q_id]['claims']['P18'][0]["mainsnak"]["datavalue"]['value']

        r3 = requests.get("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url&redirects&format=json&origin=*&titles=File:"+ urllib.parse.quote(image_url))

        for res in r3.json()['query']['pages'].values():
            for img in res['imageinfo']:
                return(img['url'])

def save_image(img_url:str, out_file:str):
    "save the person image in the out_file"
    img = requests.get(img_url, headers={"User-Agent": UA})
    format_ =  img_url.split('.')[-1]
    with open(out_file + '.' + format_, 'wb') as f:
        for chunk in img.iter_content(1024):
            f.write(chunk)
        print(f.name)


if __name__=="__main__":
    pax_name = "Georges Brassens"
    image_url = get_image_url(pax_name)
    save_image(image_url, pax_name)
