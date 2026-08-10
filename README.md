Markdown
# 🛡️ ANOS OS — Sovereign Operating System & Cybersecurity Workspace

<p align="center">
  <img src="https://img.shields.io/badge/Version-5.2-brightgreen.svg" alt="Version">
  <img src="https://img.shields.io/badge/Security-Docker%20Isolating%20Bubble-blue.svg" alt="Security">
  <img src="https://img.shields.io/badge/AI-Dual%20Ollama%20Engine-purple.svg" alt="AI">
  <img src="https://img.shields.io/badge/Architecture-Tmux%20Multi--Pane-orange.svg" alt="Architecture">
</p>

**ANOS OS** est un environnement d'exécution et de développement souverain, ultra-sécurisé et cloisonné. Basé sur un système de **bulles d'isolation Docker**, il intègre une suite complète pour le développement, le pentest, la création Web en direct et la gestion assistée par intelligence artificielle locale.

---

## 🔑 Fonctionnalités Clés

* **🛡️ Bulle d'isolation Docker (Alpine Linux) :** Cloisonnement étanche des tâches. Tout environnement créé reste isolé du système hôte et détruit ses traces temporaires à la fermeture.
* **📁 Stockage Partagé Persistant :** Montage automatique du volume `~/anos-core/stockage_partage` sur `/documents` à l'intérieur de la bulle.
* **🤖 Double Moteur IA Souverain (Ollama) :**
  * *Assistant Administrateur Système* : Génération et exécution de commandes Linux en langage naturel.
  * *Agent Pentest & Cybersécurité* : Détection automatique des requêtes orientées sécurité (Nmap, Iptables, audit réseau, etc.).
* **💻 Studio Développeur Multi-Panneaux :** Intégration native de Tmux avec gestion automatique du split-screen (Python 3, Node.js, Bash Shell).
* **🌐 Studio Web HTML/CSS avec Aperçu Temps Réel :** Éditeur Nano sur le panneau gauche et rendu visuel HTTP en direct (`links`) sur le panneau droit.
* **☠️ Suite Hacker & Monitoring Visuel :** Intégration de `cmatrix` pour la visualisation et de `htop` pour le suivi des ressources.
* **🖱️ Ergonomie Tmux Avancée :** Prise en charge native de la souris (cliquez directement sur les panneaux pour basculer) et réinitialisation automatique de la disposition.

---

## 🛠️ Architecture du Système

           +-------------------------------------------------+
           |              SYSTÈME HÔTE (Linux)               |
           +-----------------------+-------------------------+
                                   |
                                   v
           +-------------------------------------------------+
           |               ANOS OS Core Engine               |
           |             (lancer_bulle.py V5.2)              |
           +-----------+-------------------------+-----------+
                       |                         |
                       v                         v
        +------------------------------+   +-------------------+
        |     Bulle Docker Isolé      |   |  Ollama Local IA  |
        |      (Alpine Core)           |   | (Llama 3 Engine)  |
        +--------------+---------------+   +-------------------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
+-----------------------+ +-----------------------+
| /documents (Volume) | | Studio & Outils |
| ~/anos-core/stockage | | (Dev, Web, Sécurité) |
+-----------------------+ +-----------------------+


---

## 🚀 Installation & Lancement

### Prérequis

* **Linux (Ubuntu / Debian recommandé)**
* **Docker** (`sudo apt install docker.io`)
* **Tmux** (`sudo apt install tmux`)
* **Python 3**
* *(Optionnel)* **Ollama** avec le modèle `llama3` pour les fonctionnalités IA (`ollama run llama3`)

### Démarrage rapide

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/sidibemallet8-sudo/anos-core.git](https://github.com/sidibemallet8-sudo/anos-core.git)
   cd anos-core
Rendre le script exécutable :

Bash
chmod +x lancer_bulle.py
Lancer ANOS OS :

Bash
python3 lancer_bulle.py
🕹️ Utilisation et navigation
L’interface bascule automatiquement dans une session Tmux.

Navigation à la souris : Cliquez directement dans le panneau de votre choix (éditeur à gauche, aperçu/console à droite).

Clavier de Raccourcis Tmux :

Ctrl + B puis : Basculer entre les panneaux.Flèches

Ctrl + B puis : Agrandi / Réduire le panneau actif (Plein écran).Z

Ctrl + X : Quitter l’éditeur Nano et revenir au menu principal.

📜 Structure du Projet
Texte clair
anos-core/
├── lancer_bulle.py      # Script principal (Moteur ANOS OS v5.2)
├── README.md            # Documentation du projet
└── stockage_partage/    # Dossier local monté dans la bulle (/documents)
🔒 Sécurité
Tous les processus exécutés via les modules de dev, web ou IA s’exécutent au sein d’un conteneur étanche. En cas de fermeture via le menu principal (), la bulle est arrêtée et purgée du système.Option 0

📄 Licence
Ce projet est distribué sous licence sous réserve d’utilisation souveraine et sécurisée.
