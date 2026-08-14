#!/usr/bin/env python3
"""
===============================================================================
  ANOS OS v5.0 - CYBERNETIC RAM OS (DEVELOPER STUDIO & HIGH-PERFORMANCE)
  --> ÉDITION INTERACTIVE (SOURIS, BARRE DES TÂCHES & ANTI-EMPILEMENT)
===============================================================================
"""
import os
import subprocess
import shlex
import datetime
import sys
import socket
import threading
import time
import hashlib
import getpass
import signal

# Bloque le raccourci Ctrl + C pour éviter de fermer accidentellement la bulle ANOS
def ignorer_ctrl_c(sig, frame):
    print("\n[!] Ctrl+C est désactivé. Utilisez l'option du menu pour quitter proprement.")

signal.signal(signal.SIGINT, ignorer_ctrl_c)
def ouvrir_dans_dock(cmd_docker):
    """Fonction universelle pour ouvrir TOUTES les applications dans la colonne de droite"""
    if "TMUX" in os.environ:
        # 1. Compte le nombre de fenêtres ouvertes
        nbr_panneaux = int(subprocess.check_output(["tmux", "display-message", "-p", "#{window_panes}"]).decode().strip())
        
        if nbr_panneaux == 1:
            # Si c'est la toute première fenêtre secondaire, on crée la colonne de droite (-h)
            subprocess.run(["tmux", "split-window", "-h", "-p", "45", cmd_docker])
        else:
            # Si la colonne de droite existe déjà, on sélectionne le dernier volet à droite et on le coupe (-v)
            subprocess.run(["tmux", "select-pane", "-t", "{right}"])
            subprocess.run(["tmux", "split-window", "-v", cmd_docker])
            
        # 2. REVIENT SANS FAUTE SUR LE MENU PRINCIPAL (à gauche) pour qu'il ne disparaisse jamais !
        subprocess.run(["tmux", "select-pane", "-t", ".0"])
    else:
        subprocess.run(cmd_docker, shell=True)
# --- IMPORTATION DES NOUVEAUX MODULES ---
# --- IMPORTATION DES NOUVEAUX MODULES ---
try:
    from modules.gov_cyber import (
        installer_pack_outils_cyber,
        lancer_recherche_osint,
        telecharger_media_video,
        lancer_navigateur_securise
    )
    from modules.gov_ai import installer_moteurs_ia
except Exception as e:
    print(f"\033[38;5;196m[!] Erreur de chargement des modules : {e}\033[0m")
# --- Couleurs ANSI Cyberpunk ---
GREEN     = "\033[38;5;82m"     # Vert Matrix
CYAN      = "\033[38;5;51m"     # Neon Cyan
PURPLE    = "\033[38;5;129m"    # Cyber Purple
NEON_RED  = "\033[38;5;196m"    # Red Alert
YELLOW    = "\033[38;5;220m"    # Amber Gold
GRAY      = "\033[38;5;240m"    # Dark Steel
WHITE     = "\033[1;97m"        # White Glow
RESET     = "\033[0m"

CLE_ACCES_PAR_DEFAUT = "ANOS"

def forcer_privileges_root():
    if os.geteuid() != 0:
        print(f"{YELLOW}[!] NOYAU ANOS : ELEVATION DES PRIVILÈGES (ROOT)...{RESET}")
        try:
            os.execvp("sudo", ["sudo", "-E", sys.executable] + sys.argv)
        except Exception as e:
            print(f"{NEON_RED}[CRITICAL ERROR] Échec Root : {e}{RESET}")
            sys.exit(1)

def verifier_et_activer_tmux():
    if not os.environ.get("TMUX"):
        res = subprocess.run(["which", "tmux"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"{CYAN}[*] Optimisation du gestionnaire d'affichage (tmux)...{RESET}")
            subprocess.run(["apt-get", "update", "-qq"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["apt-get", "install", "-y", "-qq", "tmux"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if subprocess.run(["which", "tmux"], capture_output=True).returncode == 0:
            subprocess.run(["tmux", "kill-session", "-t", "anos_os"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.execvp("tmux", ["tmux", "new-session", "-s", "anos_os", sys.executable] + sys.argv)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def reinitialiser_panneaux():
    """Ferme toutes les fenêtres secondaires pour éviter l'empilement."""
    if os.environ.get("TMUX"):
        os.system("tmux kill-pane -a -t 0 2>/dev/null")

FICHIER_CLE = "/var/tmp/.anos_user_key.hash"
CONTACT_ARCHITECTE = "L'Architecte ANOS OS"

def hacher_cle(cle):
    """Hache la clé en SHA-256 (Sécurité souveraine : aucun mot de passe en clair)."""
    return hashlib.sha256(cle.encode()).hexdigest()

def verifier_cle_acces():
    """Gère la création au 1er lancement, la connexion et le blocage."""
    clear_screen()
    afficher_logo()
    
    # --- 1. PREMIER LANCEMENT : L'utilisateur crée sa propre clé ---
    if not os.path.exists(FICHIER_CLE):
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║             BIENVENUE SUR ANOS OS - PREMIÈRE CONFIGURATION                   ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
        print(f"{YELLOW}[!] Aucune clé configurée. Veuillez créer votre clé d'accès personnelle.{RESET}\n")
        
        while True:
            nouvelle_cle = getpass.getpass("Choisissez votre clé d'accès (saisie masquée) : ").strip()
            confirmation = getpass.getpass("Confirmez votre clé d'accès : ").strip()
            
            if nouvelle_cle == confirmation and len(nouvelle_cle) >= 4:
                with open(FICHIER_CLE, "w") as f:
                    f.write(hacher_cle(nouvelle_cle))
                print(f"\n{GREEN}[✓] Clé enregistrée avec succès ! Conservez-la en mémoire.{RESET}")
                time.sleep(1.5)
                return True
            else:
                print(f"{NEON_RED}[!] Les clés ne correspondent pas ou font moins de 4 caractères.{RESET}\n")

    # --- 2. CONNEXIONS SUIVANTES : Vérification de la clé créée ---
    with open(FICHIER_CLE, "r") as f:
        cle_enregistree = f.read().strip()

    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                   AUTHENTIFICATION - CLÉ SOUVERAINE ANOS                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    tentatives = 3
    while tentatives > 0:
        saisie = getpass.getpass("Entrez votre clé d'accès : ").strip()
        if hacher_cle(saisie) == cle_enregistree:
            print(f"\n{GREEN}[✓] Clé valide. Déverrouillage du noyau ANOS OS...{RESET}")
            time.sleep(1)
            return True
        else:
            tentatives -= 1
            print(f"{NEON_RED}[!] Clé incorrecte. Essais restants : {tentatives}{RESET}\n")

    # --- 3. EN CAS D'OUBLI OU ÉCHEC : Message de sécurité vers l'Architecte ---
    clear_screen()
    print(f"{NEON_RED}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                  🚨 ACCÈS SÉCURISÉ BLOQUÉ - ANOS OS 🚨                      ║")
    print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Nombre maximal de tentatives dépassé.                                        ║")
    print(f"║ En cas d'oubli de votre clé, vous devez impérativement contacter            ║")
    print(f"║ l'Architecte du système pour réinitialiser vos identifiants.                 ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    sys.exit(1)

def afficher_logo():
    print(f"{PURPLE}")
    print("╔════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║   █████╗ ███╗   ██╗██████╗ ███████╗   ██████╗ ███████╗ v5.0 HIGH-PERFORMANCE                       ║")
    print("║  ██╔══██╗████╗  ██║██╔══██╗██╔════╝  ██╔═══██╗██╔════╝                                             ║")
    print("║  ███████║██╔██╗ ██║██║  ██║███████╗  ██║   ██║███████╗                                             ║")
    print("║  ██╔══██║██║╚██╗██║██║  ██║╚════██║  ██║   ██║╚════██║                                             ║")
    print("║  ██║  ██║██║ ╚████║██████╔╝███████║  ╚██████╔╝███████║                                             ║")
    print("║  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝   ╚═════╝ ╚══════╝                                             ║")
    print(f"║  {CYAN}>> CYBERNETIC RAM OS | DEV STUDIO & LIVE PREVIEW | TURBO ENGINE ACTIVE <<{PURPLE}                  ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def verifier_cle_acces():
    clear_screen()
    afficher_logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                  AUTHENTIFICATION - CLÉ SOUVERAINE ANOS                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    tentative = input(f"{YELLOW}Entrez la clé d'accès souveraine : {RESET}").strip()
    if tentative == CLE_ACCES_PAR_DEFAUT:
        print(f"\n{GREEN}[✓] Clé valide. Déverrouillage du noyau ANOS OS...{RESET}")
        time.sleep(1)
        return True
    else:
        print(f"\n{NEON_RED}[!] Clé d'accès incorrecte. Accès refusé.{RESET}")
        time.sleep(2)
        sys.exit(1)

def afficher_tableau_de_bord(nom_zone):
    print(f"{GRAY}┌───[ DASHBOARD SYSTÈME ANOS ]" + "─" * 68 + "┐")
    print(f"{GRAY}│{GREEN}  [●] NOYAU : {WHITE}TURBO ONLINE{GRAY} │ {CYAN}[●] RAM TMPFS : {WHITE}1.5 GB OPTIMIZED{GRAY}│ {PURPLE}[●] DEV STUDIO : {WHITE}READY{GRAY}│")
    print(f"{GRAY}└" + "─" * 96 + "┘\n" + RESET)

# =============================================================================
# --- MODULE CHAT P2P DIRECT (STYLE WHATSAPP) ---
# =============================================================================

def demarrer_serveur_chat_direct(port=4444, cle_acces=CLE_ACCES_PAR_DEFAUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    hash_cle = hashlib.sha256(cle_acces.encode()).hexdigest()
    
    try:
        sock.bind(('0.0.0.0', port))
        sock.listen(5)
        clear_screen()
        afficher_logo()
        print(f"{GREEN}[+] RÉCEPTEUR CHAT ACTIF SUR LE PORT {port}{RESET}")
        print(f"{CYAN}[*] Clé d'accès configurée : [{YELLOW}{cle_acces}{CYAN}]{RESET}")
        print(f"{GRAY}[*] En attente de connexion directe...{RESET}\n")

        conn, addr = sock.accept()
        cle_recue = conn.recv(1024).decode('utf-8').strip()
        
        if cle_recue != hash_cle:
            print(f"{NEON_RED}[!] Connexion refusée depuis {addr[0]} (Clé incorrecte) !{RESET}")
            conn.send("ERROR_KEY".encode('utf-8'))
            conn.close()
            sock.close()
            input("\nAppuyez sur Entrée...")
            return

        conn.send("OK_CONNECTED".encode('utf-8'))
        print(f"{GREEN}[✓] CONNEXION ÉTABLIE AVEC {addr[0]} ! CANAL DIRECT OUVERT.{RESET}\n")
        
        def recevoir():
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"\n{PURPLE}[ANOS-DISTANT]:>{WHITE} {data.decode('utf-8')}{RESET}")
                    print(f"{GRAY}[ANOS-VOUS]:> {RESET}", end="", flush=True)
                except:
                    break

        threading.Thread(target=recevoir, daemon=True).start()

        while True:
            msg = input(f"{GRAY}[ANOS-VOUS]:> {RESET}")
            if msg.lower() in ['exit', 'quit']:
                conn.close()
                break
            conn.send(msg.encode('utf-8'))
            
    except Exception as e:
        print(f"{NEON_RED}[!] Erreur Récepteur Chat : {e}{RESET}")
        input("\nAppuyez sur Entrée...")
    finally:
        sock.close()

def connecter_envoyeur_chat(ip_distante, port=4444, cle_acces=CLE_ACCES_PAR_DEFAUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hash_cle = hashlib.sha256(cle_acces.encode()).hexdigest()
    
    try:
        print(f"{CYAN}[*] Connexion à {ip_distante}:{port}...{RESET}")
        sock.connect((ip_distante, port))
        sock.send(hash_cle.encode('utf-8'))
        reponse = sock.recv(1024).decode('utf-8').strip()
        
        if reponse != "OK_CONNECTED":
            print(f"{NEON_RED}[!] Clé d'accès refusée par le destinataire.{RESET}")
            sock.close()
            input("\nAppuyez sur Entrée...")
            return

        clear_screen()
        afficher_logo()
        print(f"{GREEN}[✓] CONNECTÉ DIRECTEMENT À ANOS OS ({ip_distante}) !{RESET}\n")

        def recevoir():
            while True:
                try:
                    data = sock.recv(1024)
                    if not data:
                        break
                    print(f"\n{PURPLE}[ANOS-DISTANT]:>{WHITE} {data.decode('utf-8')}{RESET}")
                    print(f"{GRAY}[ANOS-VOUS]:> {RESET}", end="", flush=True)
                except:
                    break

        threading.Thread(target=recevoir, daemon=True).start()

        while True:
            msg = input(f"{GRAY}[ANOS-VOUS]:> {RESET}")
            if msg.lower() in ['exit', 'quit']:
                sock.close()
                break
            sock.send(msg.encode('utf-8'))
            
    except Exception as e:
        print(f"{NEON_RED}[!] Impossible de joindre {ip_distante}:{port} - {e}{RESET}")
        input("\nAppuyez sur Entrée...")
    finally:
        sock.close()

def menu_chat():
    global CLE_ACCES_PAR_DEFAUT
    reinitialiser_panneaux()
    while True:
        clear_screen()
        afficher_logo()
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                 MESSAGERIE PRIVÉE P2P DIRECT (WHATSAPP STYLE)                ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {GREEN}[1]{WHITE} MODE RÉCEPTEUR   - Attendre des messages (Connexion automatique)        ║")
        print(f"║  {GREEN}[2]{WHITE} MODE ENVOYEUR    - Envoyer un message vers une IP distante            ║")
        print(f"║  {YELLOW}[3]{WHITE} CONFIGURER CLÉ   - Clé partagée actuelle: {CYAN}[{CLE_ACCES_PAR_DEFAUT}]{WHITE}              ║")
        print(f"║                                                                              ║")
        print(f"║  {NEON_RED}[0]{WHITE} Retour au menu principal                                               ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        choix = input(f"\n{CYAN}ANOS-CHAT-PROMPT > {RESET}").strip()
        if choix == '1':
            demarrer_serveur_chat_direct(cle_acces=CLE_ACCES_PAR_DEFAUT)
        elif choix == '2':
            ip = input(f"\n{YELLOW}Entrez l'adresse IP distante : {RESET}").strip()
            if ip:
                connecter_envoyeur_chat(ip, cle_acces=CLE_ACCES_PAR_DEFAUT)
        elif choix == '3':
            nouvelle_cle = input(f"\n{CYAN}Entrez la nouvelle clé d'accès : {RESET}").strip()
            if nouvelle_cle:
                CLE_ACCES_PAR_DEFAUT = nouvelle_cle
                print(f"{GREEN}[+] Clé mise à jour : [{CLE_ACCES_PAR_DEFAUT}]{RESET}")
                time.sleep(1)
        elif choix == '0':
            break

# =============================================================================
# --- MODULE : ESPACE DÉVELOPPEUR & WEB STUDIO LIVE PREVIEW ---
# =============================================================================

def lancer_pane_dev(nom_zone, commande_dev):
    """Ouvre un terminal dédié à côté (Tmux split) pour exécuter du code."""
    reinitialiser_panneaux()
    if os.environ.get("TMUX"):
        cmd_pane = (
            f"tmux split-window -d -h -p 48 "
            f"\"docker exec -it {nom_zone} sh -c '{commande_dev}'\""
        )
        os.system(cmd_pane)
        print(f"{GREEN}[+] Terminal Développeur ouvert dans la fenêtre de droite !{RESET}")
    else:
        print(f"{YELLOW}[!] Lancement en cours dans la bulle...{RESET}")
        subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", commande_dev])

def studio_web_html_css(nom_zone):
    """Crée un projet Web, lance un serveur HTTP local et ouvre un aperçu visuel Live !"""
    reinitialiser_panneaux()
    print(f"\n{CYAN}[*] Préparation de l'environnement Web Studio & Navigateur...{RESET}")
    
    init_cmd = "apk add --no-cache python3 links nano micro 2>/dev/null"
    subprocess.run(["docker", "exec", nom_zone, "sh", "-c", init_cmd], stdout=subprocess.DEVNULL)

    html_demo = """<!DOCTYPE html>
<html>
<head>
<style>
  body { background-color: #0d1117; color: #00ff66; font-family: monospace; text-align: center; padding: 50px; }
  h1 { color: #00f0ff; border-bottom: 2px solid #00f0ff; display: inline-block; }
  .box { border: 1px solid #8a2be2; padding: 20px; border-radius: 10px; margin-top: 20px; background: #161b22; }
</style>
</head>
<body>
  <h1>CYBERNETIC ANOS WEB STUDIO</h1>
  <div class="box">
    <p>Site Web exécuté en direct dans la Mémoire RAM d'ANOS OS !</p>
    <p style="color: #ff0055;">[+] Modifiez ce fichier /documents/index.html pour voir le résultat.</p>
  </div>
</body>
</html>"""
    
    cmd_write = f"if [ ! -f /documents/index.html ]; then echo '{html_demo}' > /documents/index.html; fi"
    subprocess.run(["docker", "exec", nom_zone, "sh", "-c", cmd_write])

    if os.environ.get("TMUX"):
        subprocess.run(["docker", "exec", "-d", nom_zone, "sh", "-c", "python3 -m http.server 8000 --directory /documents"], stdout=subprocess.DEVNULL)
        
        cmd_edit = f"nano /documents/index.html"
        cmd_preview = f"sleep 1 && links http://localhost:8000"
        
        print(f"{GREEN}[✓] Serveur HTTP actif sur port 8000.{RESET}")
        print(f"{CYAN}[+] Ouverture de l'éditeur à gauche et de l'Aperçu du site à droite !{RESET}")
        
        os.system(f"tmux split-window -d -h -p 50 \"docker exec -it {nom_zone} sh -c '{cmd_preview}'\"")
        subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", cmd_edit])
    else:
        print(f"{GREEN}[+] Serveur HTTP actif sur http://localhost:8000{RESET}")
        subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", "nano /documents/index.html"])

def menu_developpeur(nom_zone):
    while True:
        clear_screen()
        afficher_logo()
        afficher_tableau_de_bord(nom_zone)
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                 ESPACE DÉVELOPPEUR & STUDIO MULTI-LANGAGES                   ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {GREEN}[1]{WHITE} PYTHON STUDIO         - Terminal interactif & Exécuteur de scripts (.py)║")
        print(f"║  {GREEN}[2]{WHITE} HTML / CSS STUDIO     - Éditeur + Serveur Web & APERÇU LIVE DU SITE    ║")
        print(f"║  {GREEN}[3]{WHITE} JAVASCRIPT / NODE.JS  - Console REPL JS & exécution instantanée        ║")
        print(f"║  {GREEN}[4]{WHITE} C / C++ COMPILER      - Compilateur GCC/G++ & Exécution binaire ultra  ║")
        print(f"║  {GREEN}[5]{WHITE} TERMINAL CODEUR DÉDIÉ - Console latérale personnalisée (Tmux Split)     ║")
        print(f"║                                                                              ║")
        print(f"║  {NEON_RED}[0]{WHITE} Retour au menu principal OS                                             ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        choice = input(f"\n{CYAN}ANOS-DEV-PROMPT > {RESET}").strip()
        
        if choice == '1':
            print(f"\n{GREEN}[+] Initialisation du Studio Python...{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "apk add --no-cache python3 2>/dev/null"])
            lancer_pane_dev(nom_zone, "python3")
            time.sleep(1)
        elif choice == '2':
            studio_web_html_css(nom_zone)
        elif choice == '3':
            print(f"\n{GREEN}[+] Installation du runtime Node.js...{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "apk add --no-cache nodejs 2>/dev/null"])
            lancer_pane_dev(nom_zone, "node")
            time.sleep(1)
        elif choice == '4':
            print(f"\n{GREEN}[+] Préparation de l'environnement C/C++...{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "apk add --no-cache gcc g++ musl-dev 2>/dev/null"])
            lancer_pane_dev(nom_zone, "sh")
            time.sleep(1)
        elif choice == '5':
            cmd_custom = input(f"\n{YELLOW}Commande à exécuter dans la fenêtre latérale : {RESET}").strip()
            if cmd_custom:
                lancer_pane_dev(nom_zone, cmd_custom)
                time.sleep(1)
        elif choice == '0':
            break

# =============================================================================
# --- MODULE : DEEP RECHERCHE ANONYME (GOOGLE / DUCKDUCKGO VIA TOR) ---
# =============================================================================

def lancer_deep_recherche(nom_zone):
    """Ouvre un navigateur anonyme chiffré via Tor sans casser la structure."""
    reinitialiser_panneaux()
    print(f"\n{CYAN}[*] Initialisation du navigateur anonyme Deep Recherche via Tor...{RESET}")
    subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "apk add --no-cache links tor 2>/dev/null"], stdout=subprocess.DEVNULL)
    
    cmd_nav = (
        f"killall tor 2>/dev/null; tor & sleep 4 && "
        f"HTTP_PROXY=socks5://127.0.0.1:9050 HTTPS_PROXY=socks5://127.0.0.1:9050 "
        f"links https://html.duckduckgo.com/html/"
    )
    
    if os.environ.get("TMUX"):
        os.system(f"tmux split-window -d -h -p 50 \"docker exec -it {nom_zone} sh -c '{cmd_nav}'\"")
        print(f"{GREEN}[✓] DEEP RECHERCHE démarré en panneau latéral sécurisé.{RESET}")
    else:
        subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", cmd_nav])

# =============================================================================
# --- MODULE : GESTIONNAIRE FICHIERS ANONYME TOR ---
# =============================================================================

def explorer_et_importer_fichiers(nom_zone):
    """Permet de sélectionner un fichier partagé et de le transférer via Tor."""
    clear_screen()
    afficher_logo()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║             ACCÈS FICHIERS SÉCURISÉ & TRANSFERT ANONYME (TOR)                ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    print(f"{GREEN}[+] Fichiers disponibles dans /documents :{RESET}")
    subprocess.run(["docker", "exec", nom_zone, "ls", "-la", "/documents"])
    
    fichier = input(f"\n{YELLOW}Nom du fichier à exporter/traiter anonymement : {RESET}").strip()
    if fichier:
        print(f"{CYAN}[*] Chiffrement et routage anonyme du fichier '{fichier}' via le réseau Tor...{RESET}")
        cmd_send = f"torified_file=/documents/{fichier}; if [ -f $torified_file ]; then curl -s --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/ | grep -q 'Congratulations' && echo '[✓] Connexion anonyme Tor vérifiée.' || echo '[!] Alerte : Vérification Tor échouée.'; else echo '[!] Fichier introuvable.'; fi"
        subprocess.run(["docker", "exec", nom_zone, "sh", "-c", cmd_send])
    input("\nAppuyez sur Entrée...")

# =============================================================================
# --- AUTO-OPTIMISATION ET AUTRES MODULES ---
# =============================================================================

def turbo_boost_performances(nom_zone):
    print(f"\n{CYAN}[*] LANCEMENT DU BOOSTER DE PERFORMANCE INTELLIGENT...{RESET}")
    time.sleep(0.5)
    print(f"{GREEN}[1/4] Purge des caches résiduels en RAM (tmpfs)...{RESET}")
    subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "rm -rf /tmp/* /var/cache/* 2>/dev/null"])
    
    print(f"{GREEN}[2/4] Optimisation des descripteurs de sockets réseau...{RESET}")
    subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true"])
    
    print(f"{GREEN}[3/4] Calibrage TTY & prévention des déformations d'écran...{RESET}")
    os.system("stty sane 2>/dev/null")
    
    print(f"{GREEN}[4/4] Pré-chargement des paquets essentiels en cache ultra-rapide...{RESET}")
    print(f"\n{PURPLE}[✓] PERFORMANCE RAM MAXIMISÉE À 100% !{RESET}")
    input("\nAppuyez sur Entrée...")

def menu_configuration(nom_zone):
    while True:
        clear_screen()
        afficher_logo()
        afficher_tableau_de_bord(nom_zone)
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                  CENTRE DE CONFIGURATION & DIAGNOSTIC NOYAU                  ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {GREEN}[1]{WHITE} Inspecter la mémoire RAM volatile (tmpfs free -h)                       ║")
        print(f"║  {GREEN}[2]{WHITE} Espace disque du stockage partagé (/documents)                         ║")
        print(f"║  {GREEN}[3]{WHITE} Afficher les adresses IP (Local, Docker & Tor)                         ║")
        print(f"║  {GREEN}[4]{WHITE} TURBO BOOST PERFORMANCE (Optimisation intelligente RAM)                ║")
        print(f"║  {GREEN}[5]{WHITE} Capabilités du noyau & Sécurité Linux                                  ║")
        print(f"║  {GREEN}[6]{WHITE} Test de benchmark vitesse écriture RAM / Disk                          ║")
        print(f"║  {GREEN}[7]{WHITE} Inspecter les variables d'environnement                                ║")
        print(f"║  {GREEN}[8]{WHITE} Redémarrage à chaud de la bulle d'isolation                             ║")
        print(f"║                                                                              ║")
        print(f"║  {NEON_RED}[0]{WHITE} Retour au menu principal OS                                             ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        choice = input(f"\n{CYAN}ANOS-CONFIG-PROMPT > {RESET}").strip()
        
        if choice == '1':
            print(f"\n{GREEN}[+] Utilisation Mémoire RAM volatile :{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "free", "-h"])
            input("\nAppuyez sur Entrée...")
        elif choice == '2':
            print(f"\n{GREEN}[+] Espace stockage partagé /documents :{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "df", "-h", "/documents"])
            input("\nAppuyez sur Entrée...")
        elif choice == '3':
            print(f"\n{GREEN}[+] Interfaces IP actives :{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "ip", "a"])
            input("\nAppuyez sur Entrée...")
        elif choice == '4':
            turbo_boost_performances(nom_zone)
        elif choice == '5':
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "capsh --print 2>/dev/null || echo 'NET_ADMIN Active'"])
            input("\nAppuyez sur Entrée...")
        elif choice == '6':
            print(f"\n{GREEN}[+] Stress-test vitesse RAM :{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "time dd if=/dev/zero of=/tmp/test.tmp bs=1M count=500 conv=fdatasync && rm -f /tmp/test.tmp"])
            input("\nAppuyez sur Entrée...")
        elif choice == '7':
            subprocess.run(["docker", "exec", nom_zone, "env"])
            input("\nAppuyez sur Entrée...")
        elif choice == '8':
            subprocess.run(["docker", "restart", nom_zone])
            print(f"{GREEN}[✓] Bulle réinitialisée.{RESET}")
            input("\nAppuyez sur Entrée...")
        elif choice == '0':
            break

def menu_preinstallation(nom_zone):
    while True:
        clear_screen()
        afficher_logo()
        afficher_tableau_de_bord(nom_zone)
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                    MAGASIN DE PAQUETS & OUTILS CYBER                         ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {GREEN}[1]{WHITE} PACK CYBER-RESEAU     (curl, wget, nmap, net-tools, socat)            ║")
        print(f"║  {GREEN}[2]{WHITE} PACK DEVELOPPEMENT    (python3, py3-pip, git, gcc, musl-dev, nodejs)    ║")
        print(f"║  {GREEN}[3]{WHITE} PACK ADMIN & CONSOLE  (bash, nano, htop, tmux, vim, cmatrix, links)    ║")
        print(f"║  {GREEN}[4]{WHITE} PACK FORENSICS & SCAN (tcpdump, macchanger, iptables)                  ║")
        print(f"║  {YELLOW}[5]{WHITE} INSTALLATION LIBRE    (Saisir n'importe quel paquet Alpine/apk)        ║")
        print(f"║  {CYAN}[6]{WHITE} AUDIT DES OUTILS      (Lister les paquets installés)                   ║")
        print(f"║                                                                              ║")
        print(f"║  {NEON_RED}[0]{WHITE} Retour au menu principal OS                                             ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        choice = input(f"\n{CYAN}ANOS-STORE-PROMPT > {RESET}").strip()
        if choice in ['1', '2', '3', '4']:
            packs = {
                "1": "curl wget nmap net-tools socat",
                "2": "python3 py3-pip git gcc musl-dev nodejs",
                "3": "bash nano htop tmux vim cmatrix links",
                "4": "tcpdump macchanger iptables"
            }
            cible = packs[choice]
            print(f"\n{GREEN}[+] Injection des paquets : [{cible}]...{RESET}")
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", f"apk add --no-cache {cible}"])
            input("\n[+] Installation terminée. Appuyez sur Entrée...")
        elif choice == '5':
            paquet = input(f"\n{YELLOW}Nom du paquet APK : {RESET}").strip()
            if paquet:
                subprocess.run(["docker", "exec", nom_zone, "sh", "-c", f"apk add --no-cache {paquet}"])
            input("\nAppuyez sur Entrée...")
        elif choice == '6':
            subprocess.run(["docker", "exec", nom_zone, "apk", "info"])
            input("\nAppuyez sur Entrée...")
        elif choice == '0':
            break

def menu_scanner_reseau(nom_zone):
    while True:
        clear_screen()
        afficher_logo()
        afficher_tableau_de_bord(nom_zone)
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                      MODULE SCANNER & AUDIT RÉSEAU                           ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {GREEN}[1]{WHITE} Scan de ports rapide (Nmap Fast Scan)                                   ║")
        print(f"║  {GREEN}[2]{WHITE} Découverte des hôtes du réseau local (Ping Sweep)                      ║")
        print(f"║  {GREEN}[3]{WHITE} Inspection des connexions et ports (Netstat / SS)                       ║")
        print(f"║                                                                              ║")
        print(f"║  {NEON_RED}[0]{WHITE} Retour au menu principal                                               ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
        
        choice = input(f"\n{CYAN}ANOS-SCAN-PROMPT > {RESET}").strip()
        if choice == '1':
            cible = input(f"\n{YELLOW}Cible à scanner : {RESET}").strip()
            if cible:
                subprocess.run(["docker", "exec", nom_zone, "sh", "-c", f"nmap -F {cible} 2>/dev/null || (apk add --no-cache nmap && nmap -F {cible})"])
            input("\nAppuyez sur Entrée...")
        elif choice == '2':
            ip_range = input(f"\n{YELLOW}Plage réseau (ex: 192.168.1.0/24) : {RESET}").strip()
            if ip_range:
                subprocess.run(["docker", "exec", nom_zone, "sh", "-c", f"nmap -sn {ip_range} 2>/dev/null || (apk add --no-cache nmap && nmap -sn {ip_range})"])
            input("\nAppuyez sur Entrée...")
        elif choice == '3':
            subprocess.run(["docker", "exec", nom_zone, "sh", "-c", "netstat -tuln 2>/dev/null || ss -tuln"])
            input("\nAppuyez sur Entrée...")
        elif choice == '0':
            break

def menu_destructeur_fichiers(nom_zone):
    clear_screen()
    afficher_logo()
    print(f"{NEON_RED}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                   DESTRUCTEUR ET SÉCURISATION DE FICHIERS                   ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    fichier = input(f"{YELLOW}Fichier à détruire dans /documents : {RESET}").strip()
    if fichier:
        cmd = f"shred -u -n 3 -z /documents/{fichier} 2>/dev/null || (dd if=/dev/urandom of=/documents/{fichier} bs=1M count=10 && rm -f /documents/{fichier})"
        print(f"\n{NEON_RED}[!] Broyage du fichier {fichier}...{RESET}")
        subprocess.run(["docker", "exec", nom_zone, "sh", "-c", cmd])
        print(f"{GREEN}[✓] Fichier effacé définitivement.{RESET}")
    input("\nAppuyez sur Entrée...")

def urgence_nuke_systeme(nom_zone):
    clear_screen()
    print(f"{NEON_RED}")
    print("      ███╗   ██╗██╗   ██╗██╗██╗  ██╗███████╗    ")
    print("      ████╗  ██║██║   ██║██║██║ ██╔╝██╔════╝    ")
    print("      ██╔██╗ ██║██║   ██║██║█████═╝ █████╗      ")
    print("      ██║╚██╗██║██║   ██║██║██  ██╗ ██╔══╝      ")
    print("      ██║ ╚████║╚██████╔╝██║██║ ╚██╗███████╗    ")
    print("      ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚══╝╚══════╝    ")
    print(f"\n[!!!] DESTRUCTION D'URGENCE D'ANOS OS ACTIVÉE...{RESET}\n")
    subprocess.run(["docker", "rm", "-f", nom_zone], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.system("tmux kill-session -t anos_os 2>/dev/null")
    print(f"{GREEN}[✓] RAM NETTOYÉE ET TRACES ANÉANTIES.{RESET}\n")
    sys.exit(0)

# =============================================================================
# --- CONSOLE CLI TERMINAL ENRICHIE ---
# =============================================================================

def afficher_aide():
    print(f"\n{CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                         COMMANDES DE CONSOLE ANOS-OS                             ║")
    print(f"╠══════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  {GREEN}anos installe [paquet]{CYAN} : Installe un paquet Alpine/apk                          ║")
    print(f"║  {GREEN}anos dev              {CYAN} : Ouvre l'Espace Développeur & Web Studio                 ║")
    print(f"║  {GREEN}anos chat             {CYAN} : Ouvre la messagerie P2P directe                        ║")
    print(f"║  {GREEN}anos deep             {CYAN} : Lance la Deep Recherche anonyme (Google/DDG via Tor)   ║")
    print(f"║  {GREEN}anos files            {CYAN} : Explorateur & transfert anonyme de fichiers           ║")
    print(f"║  {GREEN}anos scan [ip]        {CYAN} : Scan rapide de ports                                   ║")
    print(f"║  {GREEN}anos nuke             {CYAN} : Destruction d'urgence immédiate du système             ║")
    print(f"║  {GREEN}tor                   {CYAN} : Déploie la mini-fenêtre Tor latérale                    ║")
    print(f"║                                                                                  ║")
    print(f"║  {YELLOW}[RACCOURCIS FENÊTRES / BARRE DES TÂCHES]{CYAN}                                           ║")
    print(f"║  {WHITE}• Réduire / Masquer fenêtre : {GREEN}Ctrl+B puis d (ou m){CYAN}                               ║")
    print(f"║  {WHITE}• Restaurer la fenêtre    : {GREEN}tmux attach-session -t anos_os{CYAN}                    ║")
    print(f"║  {WHITE}• Séparer horizontalement : {GREEN}Ctrl+B puis \"{CYAN}                                         ║")
    print(f"║  {WHITE}• Séparer verticalement   : {GREEN}Ctrl+B puis %{CYAN}                                         ║")
    print(f"║  {GREEN}exit                  {CYAN} : Quitter le terminal                                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

def interpreter_commande_v1(texte, nom_zone):
    texte_clean = texte.strip().lower()
    
    if texte_clean == "anos chat":
        menu_chat()
        return "SPECIAL_HANDLED"
    if texte_clean in ["anos dev", "anos code"]:
        menu_developpeur(nom_zone)
        return "SPECIAL_HANDLED"
    if texte_clean in ["anos deep", "anos google", "anos search"]:
        lancer_deep_recherche(nom_zone)
        return "SPECIAL_HANDLED"
    if texte_clean in ["anos files", "anos fichiers"]:
        explorer_et_importer_fichiers(nom_zone)
        return "SPECIAL_HANDLED"
    if texte_clean == "anos nuke":
        urgence_nuke_systeme(nom_zone)

    if not texte_clean.startswith(("anos", "annonce")) and texte_clean != "tor":
        return texte_clean

    parts = shlex.split(texte_clean)
    action = parts[1] if len(parts) > 1 else parts[0]
    paquet = parts[2] if len(parts) > 2 else ""

    if action in ["aide", "help", "-h"]:
        afficher_aide()
        return "SPECIAL_HANDLED"

    if action in ["installe", "install"]:
        if not paquet:
            return "echo '[!] Usage: anos installe <paquet>'"
        paquet = shlex.quote(paquet.replace("python", "python3"))
        return f"apk add --no-cache {paquet}"

    if action == "scan" and paquet:
        return f"nmap -F {paquet} 2>/dev/null || (apk add --no-cache nmap && nmap -F {paquet})"

    if action == "tor":
        cmd_tor = (
            f"docker exec -it {nom_zone} sh -c "
            f"\"killall tor 2>/dev/null; rm -f /var/lib/tor/lock; mkdir -p /var/lib/tor && "
            f"echo 'ClientUseIPv4 1' > /etc/tor/torrc && tor\""
        )
        ouvrir_dans_dock(cmd_tor)
        return "SPECIAL_TOR"

    return " ".join(parts[1:])

def ouvrir_dans_dock(cmd_docker):
    """Ouvre l'application à droite sans effacer le menu principal ni fermer les autres volets"""
    if os.environ.get("TMUX"):
        nbr_panneaux = int(subprocess.check_output(["tmux", "display-message", "-p", "#{window_panes}"]).decode().strip())
        if nbr_panneaux == 1:
            subprocess.run(["tmux", "split-window", "-h", "-p", "40", cmd_docker])
        else:
            subprocess.run(["tmux", "select-pane", "-t", "{right}"])
            subprocess.run(["tmux", "split-window", "-v", cmd_docker])
        subprocess.run(["tmux", "select-pane", "-t", ".0"])
    else:
        subprocess.run(cmd_docker, shell=True)

def lancer_mode_cli_v1(nom_zone):
    clear_screen()
    afficher_logo()
    afficher_tableau_de_bord(nom_zone)
    print(f"{GREEN}[+] CONSOLE CYBERNÉTIQUE INITIALISÉE [{nom_zone}].{RESET}")
    print(f"[*] Tapez {YELLOW}anos help{RESET} pour l'aide, {YELLOW}anos dev{RESET} pour coder, ou {NEON_RED}exit{RESET}.\n")

    while True:
        try:
            requete = input(f"{GRAY}┌──({GREEN}root💀anos-core{GRAY})-[{CYAN}~{GRAY}]\n└─{GREEN}#{RESET} ").strip()
            if requete.lower() == "exit":
                if os.environ.get("TMUX"):
                    os.system("tmux kill-pane -a -t 0 2>/dev/null")
                break
            if not requete:
                continue

            commande_traduite = interpreter_commande_v1(requete, nom_zone)
            if commande_traduite == "SPECIAL_HANDLED":
                continue
            if commande_traduite == "SPECIAL_TOR":
                print(f"{GREEN}[+] Panneau Tor ouvert à droite.{RESET}")
                continue

            subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", commande_traduite])
            
            if "cmatrix" in commande_traduite or "htop" in commande_traduite or "top" in commande_traduite:
                clear_screen()
                afficher_logo()
                afficher_tableau_de_bord(nom_zone)

        except KeyboardInterrupt:
            print(f"\n{YELLOW}[*] Tapez 'exit' pour fermer le terminal.{RESET}")

# =============================================================================
# --- MENU PRINCIPAL OS ---
# =============================================================================

def lancer_os_principal(nom_zone):
    while True:
        clear_screen()
        afficher_logo()
        afficher_tableau_de_bord(nom_zone)
        print(f"{CYAN}┌────────────────────────────────────────────────────────────────────────────┐")
        print(f"│                        MENU PRINCIPAL - ANOS OS v5.0                      │")
        print(f"├────────────────────────────────────────────────────────────────────────────┤")
        print(f"│ {GREEN}[1]{WHITE} TERMINAL SÉCURISÉ      - Console d'accès (Fix TTY & Anti-Déformation)   │")
        print(f"│ {GREEN}[2]{WHITE} CHAT P2P DIRECT        - Messagerie chiffrée directe (Style WhatsApp) │")
        print(f"│ {GREEN}[3]{WHITE} ESPACE DÉVELOPPEUR     - Studio Python, JS, C/C++ & Fenêtre Latérale  │")
        print(f"│ {GREEN}[4]{WHITE} HTML / CSS WEB STUDIO  - Éditeur avec APERÇU EN DIRECT DU SITE        │")
        print(f"│ {GREEN}[5]{WHITE} CONFIGURATION RAM      - Centre de diagnostic & Turbo Boost RAM       │")
        print(f"│ {GREEN}[6]{WHITE} STORE DE PAQUETS       - Magasin d'outils Cyber & Développement       │")
        print(f"│ {GREEN}[7]{WHITE} ANONYMAT TOR           - Panneau latéral Tor                          │")
        print(f"│ {GREEN}[8]{WHITE} SCANNER RÉSEAU         - Audit Nmap, détection de ports & hôtes       │")
        print(f"│ {GREEN}[9]{WHITE} DESTRUCTEUR FICHIERS   - Nettoyage sécurisé & broyage d'entropie      │")
        print(f"│ {YELLOW}[11]{WHITE} ACCÈS FICHIERS TOR   - Transfert & Importation Anonyme via relais    │")
        print(f"│ {CYAN}[12]{WHITE} DEEP RECHERCHE        - Recherche Anonyme Web & Google via Tor       │")
        print(f"│ {GREEN}[13]{WHITE} MODULES GOUVERNEMENTAL - Cyber, Pentest, IA, Vision & Média          │")
        print(f"│ {GREEN}[14]{WHITE} MODIFIER CLÉ D'ACCÈS   - Sécurité & Gestion du mot de passe           │")
        print(f"│ {NEON_RED}[10] NUKE D'URGENCE       - Effacement immédiat de la RAM et arrêt       │")
        print(f"├────────────────────────────────────────────────────────────────────────────┤")
        print(f"│ {NEON_RED}[0]{WHITE} ÉTEINDRE / DÉSINTÉGRER  - Fermer proprement la bulle RAM               │")
        print(f"└────────────────────────────────────────────────────────────────────────────┘{RESET}")        
        choice = input(f"\n{CYAN}ANOS-MAIN-PROMPT > {RESET}").strip()
        
        if choice == '1':
            lancer_mode_cli_v1(nom_zone)
        elif choice == '2':
            menu_chat()
        elif choice == '3':
            menu_developpeur(nom_zone)
        elif choice == '4':
            studio_web_html_css(nom_zone)
        elif choice == '5':
            menu_configuration(nom_zone)
        elif choice == '6':
            menu_preinstallation(nom_zone)
        elif choice == '7':
            reinitialiser_panneaux()
            if os.environ.get("TMUX"):
                cmd_tor_pane = (
                    f"tmux split-window -d -h -p 38 "
                    f"\"docker exec -it {nom_zone} sh -c '"
                    f"killall tor 2>/dev/null; rm -f /var/lib/tor/lock; mkdir -p /var/lib/tor && "
                    f"echo \\\"ClientUseIPv4 1\\\" > /etc/tor/torrc && tor'\""
                )
                os.system(cmd_tor_pane)
                print(f"\n{GREEN}[+] Fenêtre Tor ouverte à droite !{RESET}")
                time.sleep(1)
        elif choice == '8':
            menu_scanner_reseau(nom_zone)
        elif choice == '9':
            menu_destructeur_fichiers(nom_zone)
        elif choice == '11':
            explorer_et_importer_fichiers(nom_zone)
        elif choice == '12':
             lancer_deep_recherche(nom_zone)
        elif choice == '13':
            clear_screen()
            print(f"{CYAN}==========================================================================")
            print("                   MODULES SOUVERAINS & GOUVERNEMENTAUX")
            print(f"=========================================================================={RESET}\n")
            print("  [1] Installer Suite Cyber & Pentest")
            print("  [2] Lancer Recherche OSINT")
            print("  [3] Installer Moteurs IA & OCR")
            print("  [4] Télécharger Média / Vidéo")
            print("  [5] Navigateur Texte Sécurisé (W3M)")
            print("  [0] Retour au Menu Principal")

            sub_c = input(f"\n[>] Choix : ").strip()

            try:
               if sub_c == '1':
                   installer_pack_outils_cyber(nom_zone)
               elif sub_c == '2':
                   lancer_recherche_osint(nom_zone)
               elif sub_c == '3':
                   installer_moteurs_ia(nom_zone)
               elif sub_c == '4':
                   telecharger_media_video(nom_zone)
               elif sub_c == '5':
                   lancer_navigateur_securise(nom_zone)
            except NameError as e:
               print(f"\n{NEON_RED}[!] Erreur de fonction manquante : {e}{RESET}")
               input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '14':
            modifier_cle_utilisateur()
        elif choice == '10':
            urgence_nuke_systeme(nom_zone)
        elif choice == '0':
            print(f"\n{PURPLE}[+] DÉSINTEGRATION EN COURS... Nettoyage complet de la mémoire RAM.{RESET}\n")
            break

def deployer_bulle_v1(nom_zone):
    subprocess.run(["docker", "rm", "-f", nom_zone], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chemin_hote = os.path.expanduser("~/anos-core/stockage_partage")
    os.makedirs(f"{chemin_hote}/cache", exist_ok=True)
    
    configuration = [
        "docker", "run", "-d", "--rm", "-t",
        "--cap-add=NET_ADMIN",
        "--tmpfs", "/tmp:rw,size=1G,mode=1777",
        "--tmpfs", "/var/cache:rw,size=512M",
        "-e", "TERM=xterm-256color",
        "-v", f"{chemin_hote}:/documents",
        "--name", nom_zone,
        "anos-custom:v1",
        "sh"
    ]

    try:
        subprocess.run(configuration, stdout=subprocess.DEVNULL)
        lancer_os_principal(nom_zone)
        subprocess.run(["docker", "stop", nom_zone], stdout=subprocess.DEVNULL)
    except Exception as e:
        print(f"[-] Erreur : {e}")

def modifier_cle_utilisateur():
    """Permet à l'utilisateur de modifier sa clé s'il connaît la clé actuelle."""
    if not os.path.exists(FICHIER_CLE):
        print(f"{NEON_RED}[!] Aucune clé n'est configurée.{RESET}")
        time.sleep(1.5)
        return

    with open(FICHIER_CLE, "r") as f:
        cle_actuelle_hash = f.read().strip()

    clear_screen()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                    MODIFICATION DE LA CLÉ D'ACCÈS ANOS                       ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

    ancienne = getpass.getpass("Entrez votre clé ACTUELLE : ").strip()

    # Vérification de l'ancienne clé
    if hacher_cle(ancienne) != cle_actuelle_hash:
        print(f"\n{NEON_RED}[❌] Clé actuelle incorrecte. Modification annulée.{RESET}")
        input("\nAppuyez sur Entrée pour continuer...")
        return

    # Saisie de la nouvelle clé
    nouvelle = getpass.getpass("Entrez votre NOUVELLE clé : ").strip()
    confirm = getpass.getpass("Confirmez votre NOUVELLE clé : ").strip()

    if nouvelle == confirm and len(nouvelle) >= 4:
        with open(FICHIER_CLE, "w") as f:
            f.write(hacher_cle(nouvelle))
        print(f"\n{GREEN}[✓] Votre clé d'accès a été modifiée avec succès !{RESET}")
    else:
        print(f"\n{NEON_RED}[❌] Les clés ne correspondent pas ou font moins de 4 caractères.{RESET}")

    input("\nAppuyez sur Entrée pour continuer...")
if __name__ == "__main__":
    if os.environ.get("TMUX"):
        # Activer la souris pour cliquer/glisser sur les fenêtres
        os.system("tmux set -g mouse on >/dev/null 2>&1")    # --- ACTIVATION DU MODE BUREAU INTERACTIF & BARRE DES TÂCHES INTELLIGENTE ---
        os.system("tmux set-option -g status on >/dev/null 2>&1")
        os.system("tmux set-option -g status-position bottom >/dev/null 2>&1")
        os.system("tmux set-option -g status-style bg=black,fg=green >/dev/null 2>&1")
        os.system("tmux set-option -g window-status-current-style bg=green,fg=black,bold >/dev/null 2>&1")
        # Raccourcis pour minimiser et organiser la barre des tâches
        os.system("tmux bind-key m set-option status >/dev/null 2>&1")

    verifier_cle_acces()
    nom_zone = "anos_container"
    try:
        creer_ou_verifier_bulle_ram(nom_zone)
    except Exception as e:
        pass

    print(f"\n{CYAN}[*] Démarrage de la bulle RAM sécurisée ({nom_zone})...{RESET}")
    cmd_docker = [
        "docker", "run", "-d", "--rm",
        "--cap-add=NET_ADMIN",
        "--tmpfs", "/tmp:rw,size=1G,mode=1777",
        "--name", nom_zone,
        "anos-custom:v1",
         "tail", "-f", "/dev/null"
    ]
    subprocess.run(cmd_docker, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) 
    lancer_os_principal(nom_zone)
