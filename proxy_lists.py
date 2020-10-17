import requests
from bs4 import BeautifulSoup

URL = "https://www.proxynova.com/proxy-server-list/" 

page = requests.get(URL) #getting html of page 
soup = BeautifulSoup(page.content, 'html.parser')
table_of_servers = soup.find(id="tbl_proxy_list")


more_rows = []
one_row = []
count = 1

def sort_by_port(): 
    #sorting by port
        more_rows.sort(key=lambda x:x[1])

def sort_by_speed(): 
    #removing ms, sorting by speed and adding ms back 
        for row in more_rows:
            row[2] = list(row[2])
            row[2].pop(-2)
            row[2] = "".join(row[2])
            row[2] = int(row[2])

        more_rows.sort(key=lambda x:x[2])

        for row in more_rows:
            row[2] = str(row[2])
            row[2] = list(row[2])
            row[2].append('ms')
            row[2] = "".join(row[2])
        
def sort_by_uptime(): #removing %, sorting by uptime and adding % back
        for row in more_rows:
            row[3] = row[3].split("%")
            people = row[3][1]
            row[3] = row[3][0]
            row[3] = int(row[3])

        more_rows.sort(reverse=True, key=lambda x:x[3])

        for row in more_rows:
            row[3] = list(str(row[3]))
            row[3].append("%")
            row[3].append(people)
            row[3] = "".join(row[3])

def sort_by_rank(): # sorting by rank
    more_rows.sort(reverse=True, key=lambda x:x[5])

for i in table_of_servers.find_all("td"): 
    #extracting ip, port, speed, uptime, country, rank from html and formating them 
    text = []

    if i.script != None:
        ip_raw = str(i.script)
        ip = ip_raw.split("'")
        one_row.append(ip[1])

    for no_blank in i.text: 
        #removing blank rows and spaces
        if no_blank != "\n":
            if no_blank != " ":
                text.append(no_blank)
        
    text = "".join(text)

    if text != "": 
        #removing blank lists
        one_row.append(text)
        
    if count % 7 == 0: 
    #spliting everything on separet rows of proxy servers and their info
        more_rows.append(one_row)
        one_row = []

    if count == 84: 
    #ending loop
        break

    count += 1




sort_by = int(input("Zadejte podle čeho chcete servery řadit port, rychlost, uptime, rank!!! (1, 2, 3, 4): ")) #asking the user on type of sorting

if sort_by == 1: #type of sorting
    sort_by_port()

elif sort_by == 2:
    sort_by_speed()

elif sort_by == 3:
    sort_by_uptime()

elif sort_by == 4:
    sort_by_rank()

 
for row in more_rows: 
    #Prepandind type of proxy server
    if row[1] == "8080":
        row.insert(0, "http")
    
    elif row[1] == "80":
        row.insert(0, "http")

    elif row[1] == "1080":
        row.insert(0, "sock5")
    
    elif row[1] == "4145":
        row.insert(0, "sock5")

    else:
        row.insert(0, "http")

    row = "    ".join(row)

    print(row)

#strip
