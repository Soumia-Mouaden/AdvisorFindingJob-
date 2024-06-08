
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
from openai import OpenAI

# Configuration du navigateur Chrome pour le scraping web
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-proxy-certificate-handler')
options.add_experimental_option("detach", True)

# Appliquer les options au navigateur
browser = webdriver.Chrome(options=options)

# Initialisation des variables
myItems = []
pageN = 0

# URL de base pour la recherche d'emplois
base_url = "https://www.indeed.com/jobs?q=Data+Analyst&l=New+York%2C+NY&radius=15"

# Créez un client OpenAI avec votre token Deepinfra et endpoint
openai = OpenAI(
    api_key="BVKi8cC1MJJXHBHh3KLTaFsENj3MWzC4",
    base_url="https://api.deepinfra.com/v1/openai",
)

def extract_job_details(prompt):
    chat_completion = openai.chat.completions.create(
        model="google/gemma-1.1-7b-it",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be provided with a job description. Extract the following information: "
                    "Job Description, Start Date, End Date, Sector, Function, Experience Required, Education Level, Contract Type, Compétences."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    
    return chat_completion.choices[0].message.content.strip()

# Fonction pour extraire les détails de la description de l'emploi
def extract_job_description(job_url):
    browser.get(job_url)
    time.sleep(5)  # Attendre que la page soit entièrement chargée
    src = browser.page_source
    soup = BeautifulSoup(src, "html.parser")
    description_div = soup.find("div", id="jobDescriptionText")
    if description_div:
        return " ".join(description_div.stripped_strings)  # Join the text to remove unnecessary line breaks
    else:
        return "Description not available"

# Fonction pour extraire les colonnes des détails de l'emploi
def parse_job_details(details):
    job_info = {
        "Job Description": "N/A",
        "Start Date": "N/A",
        "End Date": "N/A",
        "Sector": "N/A",
        "Function": "N/A",
        "Experience Required": "N/A",
        "Education Level": "N/A",
        "Contract Type": "",
        "Compétences": ""
    }

    try:
        # Split lines and extract information
        lines = details.split('\n')
        current_key = None
        for line in lines:
            if line.startswith("**Job Description:**"):
                job_info["Job Description"] = line.split("**Job Description:**")[1].strip()
            elif line.startswith("**Start Date:**"):
                job_info["Start Date"] = line.split("**Start Date:**")[1].strip()
            elif line.startswith("**End Date:**"):
                job_info["End Date"] = line.split("**End Date:**")[1].strip()
            elif line.startswith("**Sector:**"):
                job_info["Sector"] = line.split("**Sector:**")[1].strip()
            elif line.startswith("**Function:**"):
                job_info["Function"] = line.split("**Function:**")[1].strip()
            elif line.startswith("**Experience Required:**"):
                job_info["Experience Required"] = line.split("**Experience Required:**")[1].strip()
            elif line.startswith("**Education Level:**"):
                job_info["Education Level"] = line.split("**Education Level:**")[1].strip()
            elif line.startswith("**Contract Type:**"):
                job_info["Contract Type"] = line.split("**Contract Type:**")[1].strip()
            elif line.startswith("**Compétences:**"):
                current_key = "Compétences"
                job_info["Compétences"] = []
            elif current_key and line.startswith("-"):
                job_info[current_key].append(line.strip("- ").strip())
        
        if isinstance(job_info["Compétences"], list):
            job_info["Compétences"] = ", ".join(job_info["Compétences"])

    except Exception as e:
        print(f"An error occurred while parsing job details: {e}")

    return job_info

# Boucle à travers les pages de résultats de recherche
for page in range(0, 30, 10):  # Parcourir 3 pages (pour test)
    url = f"{base_url}&start={page}"
    browser.get(url)
    time.sleep(5)  # Attendre que la page soit entièrement chargée
    src = browser.page_source
    soup = BeautifulSoup(src, "html.parser")
    search_results = soup.find('div', {'id': 'mosaic-provider-jobcards'})
    cards = search_results.select('ul > li .cardOutline')

    # Boucle à travers les cartes d'emploi sur la page
    for i in range(len(cards)):
        job_title = cards[i].select_one('h2')
        job_location = cards[i].select_one('.company_location')
        jobs_state_date = cards[i].select_one('[data-testid="myJobsStateDate"]')
        job_link = cards[i].select_one('a', href=True)
        
        # Check if job title, location, and link exist
        if job_title is not None and job_location is not None and job_link is not None:
            item = {
                'Job Title': job_title.text.strip(),
                'Job Location': job_location.text.strip(),
                'URL': "https://www.indeed.com" + job_link['href']  # Ajout de l'URL de l'offre
            }

            if jobs_state_date is not None:
                item['Date'] = jobs_state_date.text.strip()
            else:
                item['Date'] = "Date not available"

            job_url = item['URL']  # Utilisation de l'URL de l'offre pour extraire la description
            try:
                job_description = extract_job_description(job_url)
                print(f"Job Description: {job_description}")  # Debugging output
                job_details = extract_job_details(job_description)
                print(f"Extracted Job Details: {job_details}")  # Debugging output
                
                job_info = parse_job_details(job_details)
                print(f"Parsed Job Info: {job_info}")  # Debugging output
                
                # Vérification que les informations ont bien été extraites
                for key, value in job_info.items():
                    if value != "N/A":
                        item[key] = value
            
            except Exception as e:
                print(f"An error occurred while extracting job description: {e}")
                job_info = {}

            item.update(job_info)

            # Debugging output before adding to myItems
            print("Item to be added:", item)

            myItems.append(item)

            # Afficher les détails de l'emploi dans la console
            for key, value in item.items():
                print(f"{key}: {value}")
            print("-" * 50)

    # Afficher le numéro de la page actuelle
    print('PN' + str(page))

# Fermer le navigateur
browser.quit()

# Debugging output before writing to JSON
print("Data to be written to JSON:", myItems)

# Écrire les détails des emplois dans un fichier JSON
with open('C:\\Users\\lenovo\\WebScriping\\Soumia.json', 'w', encoding='utf-8') as mydata:
    json.dump(myItems, mydata, ensure_ascii=False, indent=4)

# Afficher le nombre total d'emplois extraits
print('Number of Jobs:', str(len(myItems)))

# Afficher un message de fin
print('Job scraping completed successfully.')
