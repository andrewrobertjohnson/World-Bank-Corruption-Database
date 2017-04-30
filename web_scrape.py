#python3 web_scrape.py
import bs4 as bs
import urllib.request
import json
import requests

data = []
errors = []
_404_ = []

base_url = 'http://star.worldbank.org/corruption-cases/node/'
node = 19776

case_id = "field-name-field-sdb-case-id"
settlement_year = "field-name-field-arw-rec-startyear"
total_sanction = "field-name-field-sdb-monetary-sanction"
sanction_type = "field-name-field-sdb-settlement-sanctions"
jurisdiction_settlement = "field-name-field-sdb-jurisdiction-settle"
foreign_public_official = "field-name-field-sdb-foreign-pub-official"
offences_alleged = "field-name-field-sdb-offenses-alleged"
offences_settled = "field-name-field-sdb-offenses-settled"
settlement_type = "field-name-field-sdb-settlement-type"
summary = "field-name-field-sdb-summary"
#url = my_url

while node < 20500:
    print(node)
    x = {}

    node_string = str(node)
    my_url = base_url + node_string
    r = requests.get(my_url)


    if r.status_code == 404:
        print(node_string + " ... " + str(404))
        _404_.append(node_string)
        node += 1
    else:
        sauce = urllib.request.urlopen(my_url).read()

        soup = bs.BeautifulSoup(sauce, 'lxml')

        name = soup.h2.text
        container_case_id = soup.find_all('div', {"class": case_id})
        container_settlement_year = soup.find_all('div', {"class": settlement_year})
        container_jurisdiction_settlement = soup.find_all('div', {"class": jurisdiction_settlement})
        container_foreign_public_official = soup.find_all('div', {"class": foreign_public_official})
        container_offences_alleged = soup.find_all('div', {"class": offences_alleged})
        container_offences_settled = soup.find_all('div', {"class": offences_settled})
        container_settlement_type = soup.find_all('div', {"class": settlement_type})
        container_total_sanction = soup.find_all('div', {"class": total_sanction})
        container_sanction_type = soup.find_all('div', {"class": sanction_type})
        container_summary = soup.find_all('div', {"class": summary})

        if not container_case_id:
            print(node_string + " ... no Case ID")
            errors.append(node_string)
            node += 1
        else:
            x["name"] = name
            x["url"] = my_url

            containers = [container_case_id, container_settlement_year, container_jurisdiction_settlement, container_foreign_public_official, container_offences_alleged, container_offences_settled, container_settlement_type, container_total_sanction, container_sanction_type, container_summary]
            for tain in containers:
                for div in tain:
                    heading = div.find('div', {'class', 'field-label'})
                    info = div.find('div', {'class', 'field-item'})
                    a = len(heading.text) - 2
                    x[heading.text[:a]] = info.text

            data.append(x)
            node +=  1

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

print(_404_)
print(errors)
