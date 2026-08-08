# ANOS (Secure Container OS)

ANOS est un système d'exploitation léger, sécurisé et isolé basé sur Docker et Alpine Linux. Il offre un environnement protégé avec des outils d'anonymisation intégrés (Tor).

---

## 🛠️ Guide d'installation et d'utilisation

Suivez ces étapes dans votre terminal pour installer et configurer ANOS sur votre machine :

### 1. Télécharger le projet
```bash
git clone [https://github.com/sidibemallet8-sudo/anos-core.git](https://github.com/sidibemallet8-sudo/anos-core.git)
cd anos-core

### 2. Construire l’image système
Bash
sudo docker build -t anos-custom:v1 .

### 3. Installer la commande globale

Pour pouvoir lancer ANOS instantanément depuis n’importe quel dossier de votre terminal :

Bash
chmod +x anos
sudo cp anos /usr/local/bin/anos

### 4. Utilisation
Ouvrez votre terminal, peu importe où vous vous trouvez, et tapez simplement :

Bash
anos

### 5. Commandes utiles à l’intérieur d’ANOS

Pour activer l’anonymisation : tapez tor
Pour quitter et nettoyer la bulle : tapez exit
pour installer un outils tapez anos install avec le nom de loutils


