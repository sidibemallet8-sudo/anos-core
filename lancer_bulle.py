#!/usr/bin/env python3
"""
ANOS - Environnement de base (Version 1 - Stable)
"""

import os
import subprocess

def afficher_logo():
    print("\033[1;32m")
    print("=================================================================")
    print("=================================================================")
    print("                                                                 ")
    print("       0 1          1     1          0 1 0 1 0        0 1 0 1 0 ")
    print("      1   0         0 1   0         1         1      1          ")
    print("     0     1        0   1 0         0         0       0 1 0 1 0 ")
    print("    1 0 1 0 1       1     0         1         1                1")
    print("   0         0      1     1          0 1 0 1 0        0 1 0 1 0 ")
    print("\033[1;32m")
    print("=================================================================")
    print("=================================================================")
    print("                                                                 ")
    print("\033[0m")
    print("WELCOME TO ANOS (V1)...\n")

def interpreter_commande_v1(texte):
    texte_clean = texte.strip()
    
    if texte_clean.lower().startswith(("anos", "annonce")):
        mots = texte_clean.split(maxsplit=1)
        if len(mots) < 2:
            return ""
        
        action = mots[1].lower()
        
        if "installe" in action or "install" in action or "ajoute" in action:
            paquet = action.replace("installe", "").replace("install", "").replace("ajoute", "").strip()
            if paquet == "python":
                paquet = "python3"
            return f"apk add --no-cache {paquet}"
        
        return action
        
    return texte_clean

def lancer_mode_cli_v1(nom_zone):
    print(f"\033[1;32m[+] Bulle [{nom_zone}] active (Version 1).\033[0m")
    print("[*] Utilisez vos outils: pour anonymiser tapez 'tor' ou tapez 'exit'.\n")

    while True:
        try:
            requete = input(f"\033[1;36m[ANOS-V1]:~$\033[0m ")
            if requete.lower() == "exit":
                break
            if not requete.strip():
                continue

            commande_traduite = interpreter_commande_v1(requete)
            
            if not commande_traduite:
                print("\033[1;31m[-] Commande vide.\033[0m")
                continue

            print(f"\033[1;33m[*] Exécution : {commande_traduite}\033[0m")

            commande_finale = f"rm -f /lib/apk/db/lock && {commande_traduite}"
            
            subprocess.run(
                ["sudo", "docker", "exec", "-it", nom_zone, "sh", "-c", commande_finale],
                text=True
            )

        except KeyboardInterrupt:
            print("\n\033[1;33m[*] Interruption utilisateur. Entrez 'exit' pour quitter proprement.\033[0m")

def deployer_bulle_v1(nom_zone):
    afficher_logo()
    print(f"[*] Amorçage de la bulle V1 : [{nom_zone}]...")

    subprocess.run(["sudo", "docker", "rm", "-f", nom_zone], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    chemin_hote = os.path.expanduser("~/anos-core/stockage_partage")
    os.makedirs(chemin_hote, exist_ok=True)
    
    # Utilisation de notre image personnalisée "anos-custom:v1" où tout est déjà installé !
    configuration = [
        "sudo", "docker", "run", "-d", "--rm", "-t",
        "--cap-add=NET_ADMIN",
        "-e", "TERM=xterm-256color",
        "-v", f"{chemin_hote}:/documents",
        "--name", nom_zone,
        "anos-custom:v1",
        "sh"
    ]

    try:
        subprocess.run(configuration, stdout=subprocess.DEVNULL)
        lancer_mode_cli_v1(nom_zone)
        subprocess.run(["sudo", "docker", "stop", nom_zone], stdout=subprocess.DEVNULL)
        print(f"\n[+] Système ANOS V1 : Zone [{nom_zone}] désintégrée. Mémoire nettoyée.")
    except Exception as e:
        print(f"[-] Erreur critique du noyau : {e}")

if __name__ == "__main__":
    deployer_bulle_v1("espace_travail")
