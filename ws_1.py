from requests_html import HTMLSession,HTML
import pandas as pd
import re
import reszletek
from bs4 import BeautifulSoup
import html
from tqdm.notebook import tqdm


def escape_li_attributes(html):
    def replacer(match):
        tag = match.group(0)
        parts = re.split(r'(".*?")', tag)
        parts = [p if i % 2 == 0 else p.replace('"', '&quot;') for i, p in enumerate(parts)]
        return ''.join(parts)

    return re.sub(r'<li\s+[^>]+>', replacer, html)

url_root = ""
if __name__ == '__main__':
    rows = []
    rows2 = []
    s = HTMLSession()
    position = 'informatikus'
    positions = {'it-programozas-fejlesztes': '10', 'it-uzemeltetes-telekommunikacio': '25'}
    page = "1"
    other_info1 = ",0,0,"
    other_info2 = "%401%401?keywordsearch"
    url = url_root+'/allasok/it-programozas-fejlesztes/' + page + ',10'
    url2a = url_root+'/allasok/'
    url2b = ',0,0,informatikus%20gazdas%c3%a1gi%20informatikus%20programoz%c3%b3%20product%20owner%20plc%20programoz%c3%b3%20informatikai%20rendszer%c3%bczemeltet%c5%91%20informatikus%20rendszergazda%20informatikai%20munkat%c3%a1rs%20informatikai%20technikus%20inform%c3%a1ci%c3%b3biztons%c3%a1gi%20szak%c3%a9rt%c5%91%20informatikai%20oktat%c3%b3%20informatikai%20%c3%bczemeltet%c5%91%20informatika%20szakos%20tan%c3%a1r%20it%20projektmenedzser%20it%20rendszergazda%20it%20gyakornok%20it%20vezet%c5%91%20it%20support%20it%20helpdesk%20munkat%c3%a1rs%20it%20support%20munkat%c3%a1rs%20it%20manager%20it%20rendszer%c3%bczemeltet%c5%91%20it%20business%20analyst%20data%20analyst%20data%20scientist%20data%20engineer%20junior%20data%20analyst%20data%20manager%20master%20data%20specialist%20data%20specialist%20governance%20%26%20data%20privacy%20expert%401%401?keywordsearch'
    url2 = url_root+'/allasok/1,0,0,informatikus%20gazdas%c3%a1gi%20informatikus%20programoz%c3%b3%20product%20owner%20plc%20programoz%c3%b3%20informatikai%20rendszer%c3%bczemeltet%c5%91%20informatikus%20rendszergazda%20informatikai%20munkat%c3%a1rs%20informatikai%20technikus%20inform%c3%a1ci%c3%b3biztons%c3%a1gi%20szak%c3%a9rt%c5%91%20informatikai%20oktat%c3%b3%20informatikai%20%c3%bczemeltet%c5%91%20informatika%20szakos%20tan%c3%a1r%20it%20projektmenedzser%20it%20rendszergazda%20it%20gyakornok%20it%20vezet%c5%91%20it%20support%20it%20helpdesk%20munkat%c3%a1rs%20it%20support%20munkat%c3%a1rs%20it%20manager%20it%20rendszer%c3%bczemeltet%c5%91%20it%20business%20analyst%20data%20analyst%20data%20scientist%20data%20engineer%20junior%20data%20analyst%20data%20manager%20master%20data%20specialist%20data%20specialist%20governance%20%26%20data%20privacy%20expert%401%401?keywordsearch'
    for position_key, position_value in positions.items():
        url = url_root+'/allasok/' + position_key + '/' + page + ',' + position_value

        requests = s.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        title = requests.html.find('title', first=True).text
        darabszam = requests.html.find('div.job-list__count', first=True)
        darabszam_divs = darabszam.find('div')
        for darabszam_div in darabszam_divs:
            if "találat" in darabszam_div.text:
                job_numbers = (int)(darabszam_div.text.replace(' db találat', '').replace('\nSzűrés',''))
                page_numbers = job_numbers // 20
                if (job_numbers % 20 > 0):
                    page_numbers += 1
                break

        print(page_numbers)

        for i in range(1, page_numbers+1):
            url = url_root+'/allasok/' + position_key + '/' + str(i) + ',' + position_value
            print(url)

            requests = s.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
            soup = BeautifulSoup(requests.text, 'html.parser')


            jobs = soup.find_all('li')
            for job in jobs:
                job_attribs = job.attrs
                if 'data-prof-id' in job.attrs:
                    job_attribs_cleaned = {}
                    for key, value in job_attribs.items():
                        if isinstance(value, str):
                            job_attribs_cleaned[key] = value.replace('"', '').strip()
                        else:
                            job_attribs_cleaned[key] = value
                    reszletezes = reszletek.reszletek()
                    rows2.append(reszletezes.setobject(job_attribs_cleaned))
                    rows.append(job_attribs_cleaned)

    requests = s.get(url2, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    title = requests.html.find('title', first=True).text
    darabszam = requests.html.find('div.job-list__count', first=True)
    darabszam_divs = darabszam.find('div')
    for darabszam_div in darabszam_divs:
        if "találat" in darabszam_div.text:
            job_numbers = (int)(darabszam_div.text.replace(' db találat', '').replace('\nSzűrés',''))
            page_numbers = job_numbers // 20
            if (job_numbers % 20 > 0):
                page_numbers += 1
            break

    print(page_numbers)

    for i in range(1, page_numbers + 1):
        print(url)
        requests = s.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        soup = BeautifulSoup(requests.text, 'html.parser')
        jobs = soup.find_all('li')
        for job in jobs:
            job_attribs = job.attrs
            if 'data-prof-id' in job.attrs:
                job_attribs_cleaned = {}
                for key, value in job_attribs.items():
                    if isinstance(value, str):
                        job_attribs_cleaned[key] = value.replace('"', '').strip()
                    else:
                        job_attribs_cleaned[key] = value
                reszletezes = reszletek.reszletek()
                rows2.append(reszletezes.setobject(job_attribs_cleaned))
                rows.append(job_attribs_cleaned)


    row3 = []
    index = -1
    for row in rows:
        index += 1
        row.update(rows2[index])
        row3.append(row)

    df = pd.DataFrame(data=row3)
    df.to_excel('dict1.xlsx')



