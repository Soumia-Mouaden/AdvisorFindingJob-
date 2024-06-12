import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from openai import OpenAI

# Configuration du client OpenAI
openai = OpenAI(
    api_key="BVKi8cC1MJJXHBHh3KLTaFsENj3MWzC4",
    base_url="https://api.deepinfra.com/v1/openai",
)

def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None

def extract_competences(profil_recherche):
    prompt = f"Extract the following information from the job profile: Compétences. Here is the profile text: {profil_recherche}"
    
    chat_completion = openai.chat.completions.create(
        model="google/gemma-1.1-7b-it",
        messages=[
            {
                "role": "system",
                "content": (
                    "You will be provided with a job profile description. Extract the following information: Compétences."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    
    competences = chat_completion.choices[0].message.content.strip()
    return competences

def scrape_and_store_data():
    base_url = "https://www.rekrute.com/offres-emploi-maroc.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    jobs_data = []

    try:
        for page in range(1, 50):  # Parcourir 1 page for testing, change to (1, 16) for full scraping
            url = f"{base_url}?page={page}"   
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            encoding = response.apparent_encoding
            html = response.content.decode(encoding, errors='ignore')
            soup = BeautifulSoup(html, "html5lib")
            posts = soup.find_all("li", class_="post-id")
            for post in posts:
                e_offre = post.find("div", class_="section")
                titleOfJob_container = e_offre.find("h2")
                titleOfJob = get_text_if_not_none(titleOfJob_container.find("a"))
                title = titleOfJob.split("|")
                titleOfJob = title[0].strip()
                holder = e_offre.find("div", class_="holder")
                entreprise = get_text_if_not_none(holder.find_all("span")[0])
                desc_poste = get_text_if_not_none(holder.find_all("span")[1])
                debut_pub_offre = get_text_if_not_none(holder.find_all("span")[2])
                fin = get_text_if_not_none(holder.find_all("span")[3])
                liste_container = e_offre.find("ul")
                secteur_activite = get_text_if_not_none(liste_container.find_all("li")[0].find("a"))
                fonction = get_text_if_not_none(liste_container.find_all("li")[1].find("a"))
                experience_requise = get_text_if_not_none(liste_container.find_all("li")[2].find("a"))
                niveau_etude_demande = get_text_if_not_none(liste_container.find_all("li")[3].find("a"))
                type_contrat_propose = get_text_if_not_none(liste_container.find_all("li")[4].find("a"))

                hreff = titleOfJob_container.find("a")
                href_detail = hreff.get("href")
                href_detaill = urljoin(base_url, href_detail)
                responsee = requests.get(href_detaill, headers=headers)
                responsee.raise_for_status()  
                encoding = responsee.apparent_encoding
                htmll = responsee.content.decode(encoding, errors='ignore')
                soupp = BeautifulSoup(htmll, "html5lib") 

                profil_texts = []
                profil_section = soupp.find_all('div', class_='blc')
                for div in profil_section:
                    h2_element = div.find('h2')
                    if h2_element and h2_element.text.strip() == 'Profil recherché :':
                        content = div.find_all(['p', 'ul'])
                        if content:
                            for item in content:
                                profil_texts.append(item.get_text(strip=True))

                profil_recherche = "\n".join(profil_texts)
                
                competences = extract_competences(profil_recherche)
                
                address_span = soupp.find('span', id='address')
                localisation = address_span.text.strip() if address_span else (title[1].strip() if len(title) > 1 else "")

                image_entrep = soupp.find('img', class_='photo')
                url_img = urljoin(base_url, image_entrep.get("src")) if image_entrep else ""

                job_data = {
                    "Title": titleOfJob,
                    "Localisation": localisation,
                    "Company": entreprise.replace('\n', ', '),
                    "Job Description": desc_poste.replace('\n', ', '),
                    "Start Date": debut_pub_offre,
                    "End Date": fin,
                    "Sector": secteur_activite,
                    "Function": fonction,
                    "Experience Required": experience_requise,
                    "Education Level": niveau_etude_demande,
                    "Contract Type": type_contrat_propose,
                    "Compétences": competences.replace('\n', ', '),
                    "Image": url_img,
                    "url_offre" : href_detaill
                }

                jobs_data.append(job_data)

    except requests.RequestException as e:
        print("Error:", e)

    json_filename = 'scraped_jobs_rekrute.json'

    with open(json_filename, 'w', encoding='UTF-8') as json_file:
        json.dump(jobs_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been written to {json_filename}")

# Schedule the task (Uncomment if scheduling is needed)
# schedule.every().monday.at("08:00").do(scrape_and_store_data)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# Run the scraping function
scrape_and_store_data()