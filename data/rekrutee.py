import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time

def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None

def scrape_and_store_data():
    base_url = "https://www.rekrute.com/offres-emploi-maroc.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    liste_titre = []
    liste_entreprise = []
    liste_desc_poste = []
    liste_debut_offre = []
    liste_fin_offre = []
    liste_secteur_activité = []
    liste_fonction = []
    liste_exp_requise = []
    liste_niveau_etude_demande = []
    liste_type_contrat = []
    liste_localisation = []

    try:
        for page in range(1, 150):   
            url = f"{base_url}?page={page}"   
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            encoding = response.apparent_encoding
            html = response.content.decode(encoding, errors='ignore')
            soup = BeautifulSoup(html, "html5lib")
            initial = soup.find("ul", id="post-data")
            posts = soup.find_all("li", class_="post-id")
            for post in posts:
                e_offre = post.find("div", class_="section")
                titleOfJob_container = e_offre.find("h2")
                titleOfJob = get_text_if_not_none(titleOfJob_container.find("a"))
                title = titleOfJob.split("|")
                titleOfJob = title[0]
                localisation = title[1]
                holder = e_offre.find("div", class_="holder")
                entreprise = get_text_if_not_none(holder.find_all("span")[0])
                desc_poste = get_text_if_not_none(holder.find_all("span")[1])
                debut_pub_offre = get_text_if_not_none(holder.find_all("span")[2])
                fin = get_text_if_not_none(holder.find_all("span")[3])
                liste_container = e_offre.find("ul")
                secteur_activite_prec = liste_container.find_all("li")[0]
                secteur_activite = get_text_if_not_none(secteur_activite_prec.find("a")) 
                fonction_prec = liste_container.find_all("li")[1]
                fonction = get_text_if_not_none(fonction_prec.find("a")) 
                experience_requise_prec = liste_container.find_all("li")[2]
                experience_requise = get_text_if_not_none(experience_requise_prec.find("a")) 
                niveau_etude_demande_prec = liste_container.find_all("li")[3]
                niveau_etude_demande = get_text_if_not_none(niveau_etude_demande_prec.find("a")) 
                type_contrat_propose_prec = liste_container.find_all("li")[4]
                type_contrat_propose = get_text_if_not_none(type_contrat_propose_prec.find("a")) 

                liste_titre.append(titleOfJob)
                liste_desc_poste.append(desc_poste)
                liste_entreprise.append(entreprise)
                liste_debut_offre.append(debut_pub_offre)
                liste_fin_offre.append(fin)
                liste_secteur_activité.append(secteur_activite)
                liste_fonction.append(fonction)
                liste_exp_requise.append(experience_requise)
                liste_niveau_etude_demande.append(niveau_etude_demande)
                liste_type_contrat.append(type_contrat_propose)
                liste_localisation.append(localisation)

    except requests.RequestException as e:
        print("Error:", e)

    csv_filename = 'scraped_jobs_rekrute.csv'

    with open(csv_filename, mode='w', newline='', encoding='UTF-8-SIG') as file:
        writer = csv.writer(file, delimiter=';')
        
        writer.writerow(['Title','localisation', 'Company', 'Job Description', 'Start Date', 'End Date', 'Sector', 'Function', 'Experience Required', 'Education Level', 'Contract Type'])
        
        for i in range(len(liste_titre)):
            writer.writerow([
                liste_titre[i],
                liste_localisation[i],
                liste_entreprise[i],
                liste_desc_poste[i],
                liste_debut_offre[i],
                liste_fin_offre[i],
                liste_secteur_activité[i],
                liste_fonction[i],
                liste_exp_requise[i],
                liste_niveau_etude_demande[i],
                liste_type_contrat[i]
            ])

    print(f"Data has been written to {csv_filename}")

# schedule.every().monday.at("08:00").do(scrape_and_store_data)

# while True:
#     schedule.run_pending()
#     time.sleep(1)  
scrape_and_store_data()