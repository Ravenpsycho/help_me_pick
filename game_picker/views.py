from typing import Any

from django.shortcuts import render
from django.views.generic import TemplateView

import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import os

load_dotenv("game_picker/env")

# Create your views here.
class MainView(TemplateView):
    template_name = "game_picker/main.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        url = "https://boardgamegeek.com/xmlapi2/collection?username=Ravenpsycho"
        headers = {"Authorization": f"Bearer {os.environ["TOKEN"]}"}
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            print("OK")
            xml_text = r.text
            with open("Ravenpsycho_collection.xml", "w", encoding="utf8") as f:
                f.writelines(xml_text)
            collection_dict = get_collection_dict("Ravenpsycho_collection.xml", ["name", "image"])
            self.collection = collection_dict
            self.name_and_pic = zip(self.collection["name"], self.collection["image"])
            print(self.collection)

def get_collection_dict(xml_file, params:list)-> dict:
    return_dict = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    games = [x for x in root]
    print(games)
    for p in params:
        return_dict[p] = [x.find(p).text for x in games]
    return return_dict
