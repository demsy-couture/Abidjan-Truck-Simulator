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

# --- 2. BASE DE DONNÉES DES STATIONS-SERVICES RÉELLES ---
stations_services_abidjan = {
    "TotalEnergies - Autoroute du Nord (Yopougon)": {"zone": "Zone Industrielle Yopougon", "prix_litre_gasoil": 715},
    "Shell - Boulevard VGE (Marcory)": {"zone": "Carrefour Playce (Marcory)", "prix_litre_gasoil": 715},
    "Ola Energy - Zone Portuaire (Treichville)": {"zone": "Port de Treichville", "prix_litre_gasoil": 715},
    "Petroci - Boulevard Latrille (Cocody)": {"zone": "Abidjan Mall (Riviera)", "prix_litre_gasoil": 715}
}

# --- 3. CATALOGUE DU CONCESSIONNAIRE DE CAMIONS ---
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

# --- 4. INITIALISATION DU PROFIL DU JOUEUR ---
profil_joueur = {
    "nom_chauffeur": "Kashif",
    "argent_fcfa": 40000000,  
    "camion_actuel": {
        "marque": "Renault Trucks",
        "modele": "Kerax d'occasion",
        "puissance_ch": 320,
        "consommation_100km": 30,
        "carburant_max_litres": 400,
        "carburant_actuel_litres": 45  # Réservoir presque vide pour tester le plein !
    },
    "camions_possedes": ["Renault Kerax d'occasion"]
}

# --- 5. ÉTAT DE LA MÉTÉO EN DIRECT ---
meteo_actuelle_abidjan = {
    "temps": "Pluie d'orage",
    "visibilite": "Basse",
    "adherence_route": 0.5
}


# --- 6. LOGIQUE DU GPS, DE LA CONDUITE ET DES STATIONS ---

def faire_le_plein(profil, nom_station):
    """Permet au joueur de s'arrêter dans une vraie station pour remplir le réservoir."""
    if nom_station not in stations_services_abidjan:
        print("❌ Station-service introuvable.")
        return
        
    station = stations_services_abidjan[nom_station]
    camion = profil["camion_actuel"]
    
    # Calcul de l'espace libre dans le réservoir
    litres_a_ajouter = camion["carburant_max_litres"] - camion["carburant_actuel_litres"]
    
    if litres_a_ajouter <= 0:
        print(f"⛽ Ton réservoir est déjà plein chez {nom_station} !")
        return
        
    coût_total = int(litres_a_ajouter * station["prix_litre_gasoil"])
    
    print(f"⛽ Arrêt chez {nom_station}...")
    print(f"Achat de {int(litres_a_ajouter)} Litres de Gasoil à {station['prix_litre_gasoil']} FCFA/L.")
    
    if profil["argent_fcfa"] >= coût_total:
        profil["argent_fcfa"] -= coût_total
        camion["carburant_actuel_litres"] = camion["carburant_max_litres"]
        print(f"✅ Plein réussi ! Coût : -{coût_total} FCFA.")
        print(f"💰 Solde restant : {profil['argent_fcfa']} FCFA\n")
    else:
        print("❌ Tu n'as pas assez d'argent pour faire le plein complet !\n")


def simuler_trajet(profil, depart, destination, poids_chargement_tonnes, gain_mission):
    """Simule la conduite en temps réel entre deux points d'Abidjan."""
    if depart in reseau_gps_abidjan and destination in reseau_gps_abidjan[depart]:
        distance = reseau_gps_abidjan[depart][destination]
    else:
        print("❌ Itinéraire introuvable sur le GPS.")
        return

    print(f"🛣️ Navigation GPS : Départ de {depart} -> Destination {destination}")
    print(f"📏 Distance : {distance} km | Chargement : {poids_chargement_tonnes} Tonnes")
    print("------------------------------------------")

    conso_base = profil["camion_actuel"]["consommation_100km"]
    conso_reelle_100km = conso_base + (poids_chargement_tonnes * 0.4)
    carburant_consomme = (distance / 100) * conso_reelle_100km
    
    # Vérification de la panne sèche
    if profil["camion_actuel"]["carburant_actuel_litres"] < carburant_consomme:
        print(f"❌ PANNE SÈCHE sur la route entre {depart} et {destination} !")
        print("⚠️ Tu as dû appeler une dépanneuse d'urgence. Frais : -50 000 FCFA.")
        profil["argent_fcfa"] -= 50000
        profil["camion_actuel"]["carburant_actuel_litres"] = 10 # Remorqué avec un fond de cuve
        print(f"💰 Solde actuel : {profil['argent_fcfa']} FCFA\n")
        return

    profil["camion_actuel"]["carburant_actuel_litres"] -= carburant_consomme
    
    # Pas de coût carburant automatique ici, car le joueur paie lui-même en station !
    amende = 0
    import random
    if random.choice([True, False]):
        amende = 10000
    
    mettre_a_jour_finances(profil, gain_mission, amende)


def mettre_a_jour_finances(profil, gain_mission, amende_infraction):
    """Calcule et affiche le bilan financier d'un trajet."""
    nouveau_solde = profil["argent_fcfa"] + gain_mission - amende_infraction
    profil["argent_fcfa"] = nouveau_solde
    
    print("==========================================")
    print("       RAPPORT DE FIN DE MISSION          ")
    print("==========================================")
    print(f"💰 Gain de la course  : +{gain_mission} FCFA")
    if amende_infraction > 0:
        print(f"⚠️ Amende Police      : -{amende_infraction} FCFA")
    print(f"👉 Solde de ton compte: {profil['argent_fcfa']} FCFA")
    print(f"⛽ Jauge Carburant    : {int(profil['camion_actuel']['carburant_actuel_litres'])} / {profil['camion_actuel']['carburant_max_litres']} Litres")
    print("==========================================\n")


# --- 7. ZONE DE TEST (Lancement du scénario de jeu) ---
if __name__ == "__main__":
    print(f"🚚 Session de conduite de {profil_joueur['nom_chauffeur']}\n")
    
    # Étape A : Le joueur commence la session avec seulement 45L de carburant.
    # Il va au Port de Treichville et décide de faire le plein avant de charger.
    faire_le_plein(profil_joueur, "Ola Energy - Zone Portuaire (Treichville)")
    
    # Étape B : Maintenant que le réservoir est plein, il prend une grosse mission vers Yopougon
    simuler_trajet(
        profil=profil_joueur,
        depart="Port de Treichville",
        destination="Zone Industrielle Yopougon",
        poids_chargement_tonnes=35,
        gain_mission=300000
    )
