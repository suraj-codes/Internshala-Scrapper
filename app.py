from email.mime import application
from flask import Flask,jsonify
import pymongo
from bs4 import BeautifulSoup
import requests
import re
app = Flask(__name__)
import db

@app.route('/')
def hello_world():
    internships = []
    for i in range(1,228):
        source = requests.get(f"https://internshala.com/internships/page-{i}").text
        soup = BeautifulSoup(source, "html.parser")
        cards = soup.find_all("div", class_="individual_internship")
        for card in cards:
            path = card.find("div",class_="profile").findChildren("a")[0]["href"]
            source1 = requests.get(f"https://internshala.com{path}")
            soup1 = BeautifulSoup(source1.text, "html.parser")
            internship = dict()
            internship["company"] = dict()
            internship["title"] = soup1.find("span",class_="profile_on_detail_page").text.strip()
            internship["company"]["name"] = soup1.find("a",class_="link_display_like_text").text.strip()
            try:
                logo = soup1.find("div",class_="internship_logo").findChildren("img")[0]["src"]
                internship["company"]["logo"] = f"https://internshala.com{logo}"
            except:
                internship["company"]["logo"] = ""
            try:
                internship["company"]["type"] = soup1.find("div",class_="ngo_tag").text.strip()
            except:
                internship["company"]["type"] = "private"
            locations = soup1.find_all("a",class_="location_link")
            internship["company"]["location"] = []
            for location in locations:
                internship["company"]["location"].append(location.text.strip())
            internship["company"]["description"] = soup1.find("div",class_="about_company_text_container").text.strip()
            try:
                internship["start_date"] = soup1.find("span",class_="start_immediately_desktop").text.strip()
            except:
                internship["start_date"] = soup1.find("div",id="start-date-first").text.strip()
            internship["duration"] = soup1.find_all("div",class_="other_detail_item")[1].findChildren("div",class_="item_body")[0].text.strip()
            internship["stipend"] = soup1.find("span",class_="stipend").text.strip()
            internship["end_date"] = soup1.find_all("div",class_="other_detail_item")[3].findChildren("div",class_="item_body")[0].text.strip()
            internship["type"] = soup1.find("div",class_="label_container_desktop").text.strip()
            internship["applicatnts"] = soup1.find("div",class_="applications_message").text.strip()
            internship["description"] = soup1.find_all("div",class_="section_heading heading_5_5")[1].find_next_sibling("div").text.strip()
            internship["forwho"] = soup1.find("div",class_="who_can_apply").text.strip()
            internship["perks"] = []
            for perk in soup1.find_all("span",class_="round_tabs"):
                internship["perks"].append(perk.text.strip())
            db.db.internships.insert_one(internship)
            internships.append(internship)
        print(f"{i} pages scraped")
    return jsonify(internships)

if __name__ == '__main__':
    app.run(debug=True)