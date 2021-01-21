from bs4 import BeautifulSoup
from theater import PurchasePeriod, Theater
from datetime import datetime

import requests
import re

base_url = "https://jkt48.com/"
theater_path = "theater/schedule?lang=id"
img_path = "/images/"
apply_url = "https://jkt48.com/ticket/apply/id/2225/type/2"
show_post_url = "https://jkt48.com/ticket/apply/id/2225/type/2/show/1?lang=id" # POST data = "payment_method=4&attribute=1&agree=1"
confirmation_url = "https://jkt48.com/ticket/apply-conf/id/2225/type/2/show/1?lang=id"
comp_url = "https://jkt48.com/ticket/apply-comp/" # POST data = "id=2225&type=2&show=1&btnSubmit.x=100&btnSubmit.y=13"

img_teamj = "icon.team1.png"
img_teamk = "icon.team2.png"
img_teamt = "icon.team5.png"
img_himawarigumi = "icon.team8.png"
img_academy = "icon.team11.png"

team_name = ["Academy Class A", "Team J", "Team KIII", "Team T", "Himawarigumi"]

def parse_schedule(raw_tags):
    columns = raw_tags[0].findAll('td')
    show_title = columns[1].text
    date_str = columns[0].contents[2]
    show_time = datetime.strptime(date_str + " " + columns[0].contents[-1].contents[0][-5:], "%d.%m.%Y %H:%M")
    ticket_time = datetime.strptime(date_str + " " + columns[0].contents[-1].contents[2][-5:], "%d.%m.%Y %H:%M")

    # create schedule for purchase time
    periods = [
        ("VIP", raw_tags[0].findAll('td')[3]),
        ("OFC", raw_tags[1].findAll('td')[1]),
        ("GEN", raw_tags[2].findAll('td')[1])
    ]
    purchase_times = []
    for title, period_tag in periods:
        period_text = period_tag.getText()
        if period_text != ' - ':
            purchase_link = period_tag.find('a').get('href') if period_tag.find('a') != None else ""
            purchase_times.append(PurchasePeriod.create_from_period_string(title, period_text, purchase_link))

    return Theater(show_title, show_time, ticket_time, purchase_times)

def parse_content(choice):
    sch = []

    img_selection = ""
    if choice == 0:
        img_selection = img_academy
    elif choice == 1:
        img_selection = img_teamj
    elif choice == 2:
        img_selection = img_teamk
    elif choice == 3:
        img_selection = img_teamt
    elif choice == 4:
        img_selection = img_himawarigumi
    else:
        pass

    r = requests.get(base_url + theater_path)
    fp = r.content

    soup = BeautifulSoup(fp, 'html.parser')
    rows = soup.find('table').findAll('tr')
    schedules = [(rows[i], rows[i+1], rows[i+2]) for i in range(1, len(rows), 3)]
    for schedule in schedules:
        team_image = schedule[0].find('img').get('src')
        if team_image.find(img_selection) != -1:
            sch.insert(0, parse_schedule(schedule))

    return sch

def main():
    for i in range(5):
        print("%d. %s" % (i+1, team_name[i]))
    choice = int(input("> ")) - 1

    team_schedule = parse_content(choice)
    print("Menampilkan %d Show untuk %s: \n" % (len(team_schedule), team_name[choice]))
    for schedule in team_schedule:
        print(schedule)

if __name__ == '__main__':
    main()
