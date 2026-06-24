# ==========================================
#      SIMULATEUR DE CAMIONS D'ABIDJAN
# ==========================================
import random

# --- 1. CONFIGURATION DU RÉSEAU GPS AVEC PANNEAUX ET PAYSAGES ---
reseau_gps_abidjan = {
    "Port de Treichville": {
        "Zone Industrielle Yopougon": {
            "distance_km": 18,
            "panneaux": ["Panneau Bleu: Direction Autoroute du Nord", "Rappel: 60 km/h Poids Lourds"],
            "paysage": "Sortie du Port, vue sur les navires, passage près du grand marché de Treichville."
        },
        "Carrefour Playce (Marcory)": {
            "distance_km": 6,
            "panneaux": ["Panneau Bleu: Marcory / Aéroport", "Indication: Pont HKB"],
            "paysage": "Axe du Boulevard VGE, traversée fluide, passage devant les grands sièges d'entreprises."
        }
    }
}

# --- 2. CONFIGURATION DES CAMIONS ---
concessionnaire_camions = {
    "entree_de_gamme": {"marque": "Renault Trucks", "modele": "Kerax d'occasion", "prix_fcfa": 15000000, "puissance_ch": 320, "consommation_100km": 30}
}

# --- 3. PROFIL DU JOUEUR ---
profil_joueur = {
    "nom_chauffeur": "Kashif",
    "argent_fcfa": 40000000,  
    "camion_actuel": {"marque": "Renault Trucks", "modele": "Kerax d'occasion", "puissance_ch": 320, "consommation_100km": 30, "carburant_max_litres": 400, "carburant_actuel_litres": 350},
    "documents_en_regle": True # Est-ce que le chauffeur a ses pièces à jour ?
}

# --- 4. LOGIQUE DES CONTROLES DE POLICE ---

def gerer_controle_police(profil):
    """Simule un contrôle de police typique sur les axes d'Abidjan."""
    type_controle = random.choice(["Radar Vitesse", "Contrôle de Pièces", "Pesage Essieu"])
    amende = 0
    
    print(f"👮 ALERTE POLICE : Sifflet ! Tu es arrêté pour un : [{type_controle}]")
    
    if type_controle == "Radar Vitesse":
        # 40% de chance d'être en excès de vitesse avec l'inertie du camion
        if random.choice([True, False, False]):
            amende = 15000
            print("⚠️ Radar : Excès de vitesse détecté sur le Boulevard ! Retrait de points virtuel.")
        else:
            print("✅ Vitesse réglementaire. Le policier te fait signe de circuler.")
            
    elif type_controle == "Contrôle de Pièces":
        if profil["documents_en_regle"]:
            print("✅ Permis, Patente et Assurance présentés. Tout est en règle. 'Bonne route chauffeur !'")
        else:
            amende = 25000
            print("❌ Défaut de pièces d'immatriculation ! Grosse amende appliquée.")
            
    elif type_controle == "Pesage Essieu":
        # Simulation d'une surcharge de marchandises
        if random.choice([True, False]):
            amende = 50000
            print("❌ Surcharge détectée sur l'essieu arrière ! Le camion abîme la route d'Abidjan.")
        else:
            print("✅ Poids conforme aux normes de la CEDEAO.")
            
    return amende

# --- 5. LOGIQUE PRINCIPALE DU TRAJET ---

def simuler_trajet_ets2(profil, depart, destination, poids_chargement_tonnes, gain_mission):
    """Simule la conduite type ETS2 avec panneaux et contrôles."""
    if depart in reseau_gps_abidjan and destination in reseau_gps_abidjan[depart]:
        route = reseau_gps_abidjan[depart][destination]
    else:
        print("❌ Route indisponible.")
        return

    print(f"🟢 MOTEUR ALLUMÉ - MISSION : {depart} ➡️ {destination}")
    print(f"👀 Visuel de départ : {route['paysage']}")
    
    print("\n🚧 PANNEAUX CROISÉS SUR LE TRAJET :")
    for panneau in route["panneaux"]:
        print(f"   [ {panneau} ]")
    
    print("\n🚙 Conduite en cours sur les axes d'Abidjan...")
    
    # Déclenchement du contrôle de police en cours de route
    amende_police = gerer_controle_police(profil)
    
    # Calcul financier final
    profil["argent_fcfa"] = profil["argent_fcfa"] + gain_mission - amende_police
    
    print("\n==========================================")
    print(f"🏁 ARRIVÉE À DESTINATION : {destination}")
    print(f"💰 Gain Mission : +{gain_mission} FCFA")
    if amende_police > 0:
        print(f"💸 Total Amendes Police : -{amende_police} FCFA")
    print(f"💳 Nouveau Solde Portefeuille : {profil['argent_fcfa']} FCFA")
    print("==========================================\n")

# --- 6. LANCEMENT ---
if __name__ == "__main__":
    simuler_trajet_ets2(profil_joueur, "Port de Treichville", "Zone Industrielle Yopougon", 35, 350000)
