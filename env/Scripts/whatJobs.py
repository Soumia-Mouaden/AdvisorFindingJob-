import requests
from bs4 import BeautifulSoup
import csv

list_titre = []
list_location = []
list_company = []
list_date = []
list_description = []
villes=[]

class Job:
    def __init__(self, title, location, company, date, description):
        self.title = title
        self.location = location
        self.company = company
        self.date = date
        self.description = description

def get_url_detail(job):
    url = job.find("a", {'class': 'a dLink bold'})['href']
    print('url :', url)
    return url

def get_job_info(url):
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    title = soup.find("div", {'class': 'dTitleSection'}).h1['title']
    location = soup.find('span', class_='wjIcon24 location').find_next_sibling(string=True).strip()
    company = soup.find('span', class_='wjIcon24 companyName').find_next_sibling(string=True).strip()
    date = soup.find('span', class_='wjIcon24 jobAge').find_next_sibling(string=True).strip()
    description = soup.find('div', class_='dDesc text-justify dPadSides py-3').get_text(separator="\n").strip()
    return Job(title, location, company, date, description)

def main():
    # baseUrl = "https://ma.whatjobs.com/all-jobs/Bouznika"
    baseUrl ="https://ma.whatjobs.com/jobs"
    for numPage in range(1, 4):
        url = f"{baseUrl}?page={numPage}"
        page = requests.get(url)
        src = page.content
        soup = BeautifulSoup(src, "lxml")
        jobs_list = soup.find_all("div", {'class': 'searchResultItem fltCls fs crPointer'})

        print("len:", len(jobs_list))
        for job_elem in jobs_list:
            job_url = get_url_detail(job_elem)
            job_info = get_job_info(job_url)
            list_titre.append(job_info.title)
            list_company.append(job_info.company)
            list_location.append(job_info.location)
            list_date.append(job_info.date)
            list_description.append(job_info.description)

    csv_filename = 'scraped_whatJobs.csv'
    try:
        with open(csv_filename, mode='w', newline='', encoding='UTF-8-SIG') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Title', 'Location', 'Company', 'Job Description', 'Date'])
            print(" len(list_titre) " , len(list_titre))
            print()
            for i in range(len(list_titre)):
                print(list_titre[i])
                writer.writerow([
                    list_titre[i],
                    list_location[i],
                    list_company[i],
                    list_description[i],
                    list_date[i]
                ])
        print(f"Data has been written to {csv_filename}")
    except Exception as e:
        print(f"Failed to write to CSV file {csv_filename}: {e}")

if __name__ == "__main__":
    main()