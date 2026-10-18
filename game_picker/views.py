from typing import Any

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv
import os

from game_picker.forms import BGGUserForm

load_dotenv("game_picker/env")

class MainView(TemplateView):
    template_name = "game_picker/main.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
    def get_context_data(self, **kwargs):
        print(kwargs)
        if "username" in kwargs.keys():
            self.collection = get_user_collection(kwargs["username"])
        else:
            self.collection = get_user_collection()
        self.name_and_pic = zip(self.collection["name"], self.collection["image"])
        self.form = BGGUserForm()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        p = request.POST
        return HttpResponseRedirect(f"user={p["username"]}")

def get_collection_dict(xml_file, params:list)-> dict:
    return_dict = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    games = [x for x in root]
    for p in params:
        return_dict[p] = [x.find(p).text for x in games]
    return return_dict

def get_user_collection(username:str="Ravenpsycho"):
    url = f"https://boardgamegeek.com/xmlapi2/collection?username={username}"
    headers = {"Authorization": f"Bearer {os.environ["TOKEN"]}"}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        xml_text = r.text
        with open(f"{username}_collection.xml", "w", encoding="utf8") as f:
            f.writelines(xml_text)
        collection_dict = get_collection_dict(f"{username}_collection.xml", ["name", "image"])
        return collection_dict
    return {}