# ==========================================
#      SIMULATEUR DE CAMIONS D'ABIDJAN
# ==========================================

# --- 1. CONFIGURATION DU RÉSEAU GPS D'ABIDJAN (Distances réelles en km) ---
reseau_gps_abidjan = {
    "Port de Treichville": {
        "Zone Industrielle Yopougon": 18,
        "Zone Industrielle Koumassi": 12,
        "Abidjan Mall (Riviera)": 15,
        "Carrefour Playce (Marcory)": 6,
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

# --- 3. INITIALISATION DU PROFIL DU JOUEUR ---
profil_joueur = {
    "nom_chauffeur": "Kashif",
    "argent_fcfa": 40000000,  # 40 Millions CFA de départ pour nos tests
    "camion_actuel": {
        "marque": "Renault Trucks",
        "modele": "Kerax d'occasion",
        "puissance_ch": 320,
        "consommation_100km": 30,
        "carburant_max_litres": 400,
        "carburant_actuel_litres": 200
    },
    "camions_possedes": ["Renault Kerax d'occasion"]
}

# --- 4. ÉTAT DE LA MÉTÉO EN DIRECT ---
meteo_actuelle_abidjan = {
    "temps": "Pluie d'orage",
    "visibilite": "Basse",
    "adherence_route": 0.5  # La route glisse, attention aux freinages !
}


# --- 5. LOGIQUE DU GPS ET DE LA CONDUITE ---

def simuler_trajet(profil, depart, destination, poids_chargement_tonnes, gain_mission):
    """Simule la conduite en temps réel entre deux points d'Abidjan."""
    
    # Vérifier si la route existe dans le GPS
    if depart in reseau_gps_abidjan and destination in reseau_gps_abidjan[depart]:
        distance = reseau_gps_abidjan[depart][destination]
    else:
        print("❌ Itinéraire introuvable sur le GPS.")
        return

    print(f"🛣️ Navigation GPS : Départ de {depart} -> Destination {destination}")
    print(f"📏 Distance : {distance} km | Chargement : {poids_chargement_tonnes} Tonnes")
    print(f"🌧️ Météo actuelle : {meteo_actuelle_abidjan['temps']} (Adhérence : {meteo_actuelle_abidjan['adherence_route']})")
    print("------------------------------------------")

    # Calcul de la consommation réelle (plus le camion est lourd, plus il consomme)
    conso_base = profil["camion_actuel"]["consommation_100km"]
    conso_reelle_100km = conso_base + (poids_chargement_tonnes * 0.4)
    carburant_consomme = (distance / 100) * conso_reelle_100km
    
    # Vérification du réservoir
    if profil["camion_actuel"]["carburant_actuel_litres"] < carburant_consomme:
        print("❌ Panne sèche en plein trajet ! Tu as dû payer une dépanneuse (-50 000 FCFA).")
        profil["argent_fcfa"] -= 50000
        return

    # Mise à jour du réservoir
    profil["camion_actuel"]["carburant_actuel_litres"] -= carburant_consomme
    
    # Simulation des frais de carburant (Ex: 700 FCFA le litre de gasoil)
    coût_carburant = int(carburant_consomme * 700)
    
    # Simulation d'une amende aléatoire (Ex: radar de vitesse sur le Boulevard VGE ou l'Autoroute)
    amende = 0
    import random
    if random.choice([True, False]): # 50% de chance d'avoir un contrôle de police
        amende = 10000
    
    # Calcul du bilan financier final
    mettre_a_jour_finances(profil, gain_mission, coût_carburant, amende)


def mettre_a_jour_finances(profil, gain_mission, depense_carburant, amende_infraction):
    """Calcule et affiche le bilan financier d'un trajet."""
    nouveau_solde = profil["argent_fcfa"] + gain_mission - depense_carburant - amende_infraction
    profil["argent_fcfa"] = nouveau_solde
    
    print("==========================================")
    print("       RAPPORT DE FIN DE MISSION          ")
    print("==========================================")
    print(f"💰 Gain de la course  : +{gain_mission} FCFA")
    print(f"⛽ Coût du gasoil     : -{depense_carburant} FCFA")
    if amende_infraction > 0:
        print(f"⚠️ Amende Police      : -{amende_infraction} FCFA")
    print(f"👉 Solde de ton compte: {profil['argent_fcfa']} FCFA")
    print(f"⛽ Réservoir restant  : {int(profil['camion_actuel']['carburant_actuel_litres'])} Litres")
    print("==========================================\n")


def tentative_achat_camion(profil, categorie_camion):
    """Gère le processus d'achat d'un nouveau véhicule."""
    camion_choisi = concessionnaire_camions[categorie_camion]
    prix = camion_choisi["prix_fcfa"]
    nom_complet = f"{camion_choisi['marque']} {camion_choisi['modele']}"
    
    print(f"🛒 Concessionnaire : Tentative d'achat de {nom_complet}...")
    
    if profil["argent_fcfa"] >= prix:
        profil["argent_fcfa"] -= prix
        profil["camions_possedes"].append(nom_complet)
        profil["camion_actuel"] = camion_choisi
        print(f"🎉 Succès ! Tu as acheté le {nom_complet}. C'est ton nouveau véhicule actif.")
        print(f"💰 Nouveau solde : {profil['argent_fcfa']} FCFA\n")
    else:
        manque = prix - profil["argent_fcfa"]
        print(f"❌ Échec ! Solde insuffisant. Il te manque {manque} FCFA.\n")


# --- 6. ZONE DE TEST (Lancement du jeu) ---
if __name__ == "__main__":
    print(f"🚚 Bienvenue sur les routes d'Abidjan, Chauffeur {profil_joueur['nom_chauffeur']} !\n")
    
    # Mission 1 : Partir du Port de Treichville pour livrer 32 Tonnes au Carrefour Playce Marcory
    simuler_trajet(
        profil=profil_joueur,
        depart="Port de Treichville",
        destination="Carrefour Playce (Marcory)",
        poids_chargement_tonnes=32,
        gain_mission=250000  # Payé 250 000 FCFA
    )
    
    # Mission 2 : Tenter d'acheter le Mercedes-Benz Actros chez le concessionnaire
    tentative_achat_camion(profil_joueur, "milieu_de_gamme")
