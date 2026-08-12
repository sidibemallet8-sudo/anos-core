# 🛡️ ANOS OS v5.0 - Cybernetic RAM OS

**ANOS OS** est un système d'exploitation souverain, léger et ultra-sécurisé s'exécutant dans un environnement isolé en mémoire RAM via des conteneurs Docker et Tmux.

---

## 🚀 Fonctionnalités Principales

- **🛡️ Bulle d'Isolation Volatile** : Exécution isolée en RAM (`tmpfs`), effacement complet des traces et données lors de la fermeture.
- **💻 Studio Développeur Multi-Fenêtres** : Support de Python, HTML/CSS (avec aperçu Live HTTP), JavaScript (Node.js) et C/C++.
- **💬 Messagerie P2P Directe** : Canal de communication privé de pair-à-pair chiffré par clé partagée.
- **🌐 Deep Recherche & Anonymat Tor** : Navigation et recherches anonymes chiffrées via les relais SOCKS5 de Tor.
- **📁 Gestionnaire de Fichiers Chiffré** : Importation/exportation anonymisée de documents.
- **🛠️ Magasin de Paquets & Diagnostic** : Installation de paquets Alpine (`apk`), scanner de ports (`Nmap`) et outils de diagnostic noyau.
- **🚨 Destruction d'Urgence (Nuke)** : Purge immédiate de la mémoire RAM et arrêt critique du système.

---

## 🛠️ Prérequis

- Linux (Ubuntu Server / Debian / WSL2)
- Docker
- Tmux
- Python 3

---

## 📦 Installation & Lancement

1. **Cloner le projet :**
   ```bash
   cd ANOS-OS
Rendre le script exécutable et lancer ANOS OS :

Bash
chmod +x lancer_bulle.py
sudo ./lancer_bulle.py
Clé d’accès par défaut :

Texte clair
ANOS-KEY-2026
🎮 Raccourcis Clavier (Gestion des Fenêtres)
Minimiser / Masquer la fenêtre : puis (ou Ctrl + Bmd)

Restaurer la session : tmux attach-session -t anos_os

Diviser l’écran horizontalement : puis Ctrl + B"

Diviser l’écran verticalement : puis Ctrl + B%

📜 Licence
Projet Souverain ANOS OS - Tous droits réservés.
