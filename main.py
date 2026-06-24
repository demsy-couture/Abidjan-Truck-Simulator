# ==========================================
#      SIMULATEUR DE CAMIONS D'ABIDJAN
# ==========================================
import random

# --- 1. CONFIGURATION DU RÉSEAU GPS AVEC PAYSAGES, PANNEAUX ET PÉAGES ---
reseau_gps_abidjan = {
    "Port de Treichville": {
        "Zone Industrielle Yopougon": {
            "distance_km": 18,
            "panneaux": [
                "Panneau Bleu: Direction Gagnoa / Yamoussoukro / Autoroute du Nord", 
                "Rappel: 60 km/h Zone Urbaine Poids Lourds",
                "Panneau Pub: SOLIBRA - L'ambiance nationale"
            ],
            "peage_nom": "Péage d'Attinguié (Zone de transition)",
            "peage_cout_fcfa": 2500, # Tarif classe 3/4 pour les gros camions
            "paysage": "Traversée de la lagune Ébrié, passage sous le Pont Haubané, évitement des Gbakas pressés."
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
    "documents_en_regle": True
}

# --- 4. LOGIQUE DES CONTROLES ET INFRACTIONS (SYSTÈME IVOIRIEN) ---

def gerer_controle_police_strict(profil):
    """Simule les interactions réelles avec les forces de l'ordre à Abidjan."""
    type_controle = random.choice(["Gendarmerie Nationale", "Police de la Circulation", "Contrôle de l'Oser"])
    amende = 0
    
    print(f"\n👮 ALERT POLICE : Un agent de la [{type_controle}] lève son sifflet au loin et te fait signe de te garer !")
    
    # Choix du joueur : Décider de s'arrêter ou de fuir (Simulé de manière aléatoire pour le test)
    # Dans le jeu final, ce sera un vrai bouton à cliquer.
    decision_joueur = random.choice(["S'ARRÊTER", "FUIR_LE_SIFFLET"])
    
    if decision_joueur == "FUIR_LE_SIFFLET":
        amende = 100000  # Grosse amende de 100 000 FCFA pour refus d'obtempérer !
        print("🚨 INFRACTION GRAVE ! Tu as ignoré le sifflet du policier !")
        print(f"💸 Refus d'obtempérer détecté par caméra : Prélèvement automatique de -{amende} FCFA sur ton compte.")
        return amende

    # Si le joueur s'est arrêté sagement
    print("🚛 Tu coupes ton moteur et tu descends la vitre avec respect.")
    motif = random.choice(["Contrôle Routier Routine", "Radar Vitesse VGE/Autoroute", "Pesage Essieu Surcharge"])
    
    if motif == "Contrôle Routier Routine":
        if profil["documents_en_regle"]:
            print("✅ 'Vos pièces sont à jour, Chauffeur. Circulez, bonne route !'")
        else:
            amende = 25000
            print("❌ Défaut de pièces de transport. Amende forfaitaire appliquée.")
            
    elif motif == "Radar Vitesse VGE/Autoroute":
        # Excès de vitesse
        amende = 15000
        print(f"⚠️ Flashé par le radar ! Tu roulais trop vite. L'amende s'élève à -{amende} FCFA.")
        
    elif motif == "Pesage Essieu Surcharge":
        # Surcharge de tonnes
        amende = 50000
        print(f"❌ La balance indique que ton camion dépasse le tonnage autorisé ! Amende : -{amende} FCFA.")
        
    return amende

# --- 5. LOGIQUE PRINCIPALE DE CONDUITE TYPE ETS2 ---

def simuler_trajet_abidjan_complet(profil, depart, destination, poids_chargement_tonnes, gain_mission):
    if depart in reseau_gps_abidjan and destination in reseau_gps_abidjan[depart]:
        route = reseau_gps_abidjan[depart][destination]
    else:
        print("❌ Destination non connectée.")
        return

    print(f"🚚 [MOTEUR ALLUMÉ] - DEPART : {depart} ➡️ DESTINATION : {destination}")
    print(f"👀 Vue Pare-brise : {route['paysage']}")
    
    print("\n🚥 Signalisation en direct :")
    for panneau in route["panneaux"]:
        print(f"   [ {panneau} ]")
        
    # Passage obligatoire au péage réel
    print(f"\n🛑 Arrêt obligatoire au {route['peage_nom']}.")
    print(f"🪙 Paiement de la taxe d'infrastructure : -{route['peage_cout_fcfa']} FCFA.")
    profil["argent_fcfa"] -= route["peage_cout_fcfa"]

    # Le contrôle de police surprise sur la route
    frais_police = gerer_controle_police_strict(profil)
    
    # Calcul du salaire
    profil["argent_fcfa"] = profil["argent_fcfa"] + gain_mission - frais_police
    
    print("\n==========================================")
    print(f"🏁 DÉCHARGEMENT EFFECTUÉ À : {destination}")
    print(f"💰 Salaire brut de la course : +{gain_mission} FCFA")
    if frais_police > 0:
        print(f"👮 Retenues pour infractions  : -{frais_police} FCFA")
    print(f"💳 Solde disponible en banque : {profil['argent_fcfa']} FCFA")
    print("==========================================\n")

# --- 6. SIMULATION ---
if __name__ == "__main__":
    simuler_trajet_abidjan_complet(profil_joueur, "Port de Treichville", "Zone Industrielle Yopougon", 40, 500000)
