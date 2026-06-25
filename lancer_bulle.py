import os
import subprocess
import sys

def deployer_bulle_complete_anos(nom_zone):
    print(f"[*] Amorçage de la zone : [{nom_zone}]...")
    # Code à ajouter au début du fichier lancer_bulle.py
    print("\033[1;32m")  # Active la couleur verte
    print("       0 1          1     1    1        0 1 0 1 0        0 1 0 1 0 ")
    print("      1   0         0 1   0    0       1         1      1         0")
    print("     0     1        0   1 0    1       0         0       0 1 0 1 0 ")
    print("    1 0 1 0 1       1     0    0       1         1                1")
    print("   0         0      1     1    1        0 1 0 1 0        0 1 0 1 0 ")
    print("\033[0m")       # Réinitialise la couleur par défaut du terminal
    print("WELCOME to  ANOS Environment...\n")
     
    # Chemin absolu du dossier de stockage sur Ubuntu
    chemin_hote = os.path.expanduser("~/anos-core/stockage_partage")
    ip_espion = "1.1.1.1"
    
    # Configuration de la défense réseau + accueil du stockage
    script_securite = f"""
    echo '[*] Armement du pare-feu et montage du disque Anos...'
    apk update > /dev/null && apk add iptables > /dev/null
    iptables -A OUTPUT -d {ip_espion} -j DROP
    echo '[+] Espace de stockage sécurisé monté sur /documents'
    echo '[!] Mode blindé opérationnel. Entrée dans la zone.'
    sh
    """
    
    # -v {chemin_hote}:/documents : Connecte le dossier réel au dossier virtuel de la bulle
    configuration = [
        "sudo", "docker", "run", 
        "--rm", 
        "-it", 
        "--cap-add=NET_ADMIN",
        "-v", f"{chemin_hote}:/documents",
        "--name", nom_zone, 
        "alpine", "sh", "-c", script_securite
    ]
    
    try:
        subprocess.run(configuration)
        print(f"\n[+] Système Anos : Zone [{nom_zone}] désintégrée. Mémoire nettoyée.")
    except Exception as e:
        print(f"[-] Erreur critique du noyau : {e}")

if __name__ == "__main__":
    deployer_bulle_complete_anos("espace_travail_gouvernemental")
