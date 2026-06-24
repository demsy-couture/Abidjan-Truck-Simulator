# ==========================================
#      SIMULATEUR DE CAMIONS D'ABIDJAN
# ==========================================

# --- 1. CONFIGURATION DU RÉSEAU GPS D'ABIDJAN (Distances en km) ---
reseau_gps_abidjan = {
    "Port de Treichville": {
        "Zone Industrielle Yopougon": 18,
        "Zone Industrielle Koumassi": 12,
        "Abidjan Mall (Riviera)": 15,
        "Centre Commercial CAP SUD (Marcory)": 6,
        "Playce Palmeraie": 17
    },
    "Zone Industrielle Yopougon": {
        "Port de Treichville": 18,
        "Zone Industrielle Koumassi": 28,
        "Auchan Abobo Samake": 12
    },
    "Auchan Abobo Samake": {
        "Zone Industrielle Yopougon": 12,
        "Port de Treichville": 16
    }
}

# --- 2. CATALOGUE DU CONCESSIONNAIRE DE CAMIONS ---
concessionnaire_camions = {
    "entree_de_gamme": {
        "marque": "Renault Trucks",
        "modele": "Kerax d'occasion",
        "prix_fcfa": 15000000,
        "puissance_ch": 320,
        "consommation_100km": 30
    },
    "milieu_de_gamme": {
        "marque": "Mercedes-Benz",
        "modele": "Actros 2040",
        "prix_fcfa": 35000000,
        "puissance_ch": 400,
        "consommation_100km": 35
    },
    "haut_de_gamme_ultime": {
        "marque": "Volvo",
        "modele": "FH16 Globetrotter",
        "prix_fcfa": 75000000,
        "puissance_ch": 750,
        "consommation_100km": 42
    }
}

# --- 3. INITIALISATION DU PROFIL DU JOUEUR (Nouveau conducteur) ---
profil_joueur = {
    "nom_chauffeur": "Kashif",
    "argent_fcfa": 40000000,  # 40 Millions CFA pour tester les fonctionnalités
    "camion_actuel": {
        "marque": "Renault Trucks",
        "modele": "Kerax d'occasion",
        "puissance_ch": 320,
        "consommation_100km": 30
    },
    "camions_possedes": ["Renault Kerax d'occasion"]
}

# --- 4. ENREGISTREMENT DE LA MÉTÉO EN TEMPS RÉEL ---
meteo_actuelle_abidjan = {
    "temps": "Pluie d'orage",
    "visibilite": "Basse",
    "adherence_route": 0.5  # La route glisse !
}


# --- 5. LOGIQUE DES FONCTIONS DU JEU ---

def mettre_a_jour_finances(profil, gain_mission, depense_carburant, amende_infraction):
    """Calcule et affiche le bilan financier d'un trajet."""
    nouveau_solde = profil["argent_fcfa"] + gain_mission - depense_carburant - amende_infraction
    profil["argent_fcfa"] = nouveau_solde
    
    print("==========================================")
    print("       RAPPORT DE FIN DE MISSION          ")
    print("==========================================")
    print(f"💰 Gain de la course : +{gain_mission} FCFA")
    print(f"⛽ Carburant consommé : -{depense_carburant} FCFA")
    if amende_infraction > 0:
        print(f"⚠️ Police (Infraction) : -{amende_infraction} FCFA")
    print(f"👉 Solde actuel du compte : {profil['argent_fcfa']} FCFA")
    print("==========================================\n")


def tentative_achat_camion(profil, categorie_camion):
    """Gère le processus d'achat d'un nouveau véhicule."""
    camion_choisi = concessionnaire_camions[categorie_camion]
    prix = camion_choisi["prix_fcfa"]
    nom_complet = f"{camion_choisi['marque']} {camion_choisi['modele']}"
    
    print(f"🛒 Tentative d'achat du véhicule : {nom_complet}...")
    print(f"Prix demandé : {prix} FCFA | Votre solde : {profil['argent_fcfa']} FCFA")
    
    if profil["argent_fcfa"] >= prix:
        profil["argent_fcfa"] -= prix
        profil["camions_possedes"].append(nom_complet)
        profil["camion_actuel"] = camion_choisi
        print(f"🎉 Succès ! Vous roulez désormais en {nom_complet}.")
        print(f"💰 Nouveau solde : {profil['argent_fcfa']} FCFA\n")
    else:
        manque = prix - profil["argent_fcfa"]
        print(f"❌ Échec ! Solde insuffisant. Il vous manque {manque} FCFA.\n")


# --- 6. SIMULATION D'UNE SESSION DE JEU (Zone de Test) ---
if __name__ == "__main__":
    print(f"🚚 Bienvenue dans le simulateur, Chauffeur {profil_joueur['nom_chauffeur']} !\n")
    
    # Simulation 1 : Fin d'une mission difficile sous la pluie d'Abidjan
    # (Départ Port de Treichville -> Livraison Auchan Abobo Samaké)
    mettre_a_jour_finances(
        profil=profil_joueur, 
        gain_mission=180000, 
        depense_carburant=35000, 
        amende_infraction=10000  # Amende pour excès de vitesse sur la route d'Abobo
    )
    
    # Simulation 2 : Le joueur tente d'acheter le Mercedes-Benz Actros (35M FCFA)
    tentative_achat_camion(profil_joueur, "milieu_de_gamme")
    
    # Simulation 3 : Le joueur tente directement d'acheter le Volvo ultime (75M FCFA)
    tentative_achat_camion(profil_joueur, "haut_de_gamme_ultime")
