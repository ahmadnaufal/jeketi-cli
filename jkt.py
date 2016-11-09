from BeautifulSoup import BeautifulSoup
import requests
import theater

base_url = "http://jkt48.com/"
theater_path = "theater/schedule?lang=id"
img_path = "/images/"
img_teamj = "icon.team1.png"
img_teamk = "icon.team2.png"
img_teamt = "icon.team5.png"
img_himawarigumi = "icon.team8.png"
img_trainee = "icon.team10.png"

team_name = ["Trainee", "Team J", "Team KIII", "Team T", "Himawarigumi"]

def parse_content(choice):
    sch = []

    img_selection = ""
    if choice == 0:
        img_selection = img_trainee
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

    soup = BeautifulSoup(r.content)
    rows = soup.find('table').findAll('tr')
    schedules = [rows[i] for i in range(1, len(rows), 6)]
    team_schedules = [x for x in schedules if x.find('img',{'src': img_path + img_selection})]
    for team_schedule in team_schedules:
        sch.insert(0,theater.Theater(team_schedule))

    return sch

def main():
    for i in xrange(5):
        print "%d. %s" % (i, team_name[i])
    choice = int(raw_input("> "))

    team_schedule = parse_content(choice)
    print "Menampilkan %d Show untuk %s: \n" % (len(team_schedule),team_name[choice])
    for schedule in team_schedule:
        print schedule.print_schedule()

if __name__ == '__main__':
    main()
