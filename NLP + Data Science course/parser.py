from bs4 import BeautifulSoup
import requests
import csv

def parser():
    url = 'http://notelections.online/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222'
    base_url = 'http://notelections.online'
    html = requests.get(url).content.strip()
    bs = BeautifulSoup(html, "html.parser")
    tiks_refs = bs.find_all("a")[8:-4]
    do_ones = True
    global_list = []
    with open('election.csv', mode='w') as election_csv:
        csv_writer = csv.writer(election_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for ref in tiks_refs: 
            tik_name = ref.contents[0]
            tik_html = requests.get(base_url + ref.get('href')).content.strip() 
            bs_2 = BeautifulSoup(tik_html, "html.parser")
            if do_ones: 
                csv_header = ['ТИК', 'УИК']
                col_names = bs_2.find_all('table')[2].find_all('td')[3].find_all('td')[7].find_all('td', {'align': 'left'})
                for nm in col_names: 
                    csv_header.append(nm.getText())
                csv_writer.writerow(csv_header)
                do_ones = False
            rows = []
            links_cont = len(bs_2.find_all("a"))
            yiks_count = links_cont - 12
            rows.append([tik_name] * yiks_count) 
            for i in range (12):
                row = []
                html_row = bs_2.find_all('table')[2].find_all('td')[59 + i * yiks_count : 59 + (i + 1) * yiks_count]  
                for r in html_row: 
                    row.append(r.getText().replace('\n', ''))
                rows.append(row) 
            for i in range(12,15):
                row = []
                html_row = bs_2.find_all('table')[2].find_all('td')[59 + i * yiks_count + 2: 59 + (i + 1) * yiks_count + 2]  
                for r in html_row: 
                    row.append(r.getText().split('\n')[0])
                rows.append(row) 
            global_list += list(map(list, zip(*rows)))
        for row in global_list: 
            csv_writer.writerow(row)