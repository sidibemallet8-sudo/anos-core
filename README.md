# ANOS (Secure Container OS)

ANOS est un système d'exploitation léger, sécurisé et isolé basé sur Docker et Alpine Linux. Il offre un environnement protégé avec des outils d'anonymisation intégrés (Tor).

---

## 🛠️ Guide d'installation et d'utilisation pour les débutants

Si vous découvrez le projet et souhaitez l'installer sur votre machine, suivez ces étapes pas à pas dans votre terminal :

### 1. Télécharger le projet sur votre ordinateur
Ouvrez votre terminal et tapez ces commandes pour cloner le dépôt :
```bash
git clone [https://github.com/sidibemallet8-sudo/anos-core.git](https://github.com/sidibemallet8-sudo/anos-core.git)
cd anos-core
### 2. Construire l’image système personnalisée (⚠️ Étape obligatoire)
Cette étape permet de fabriquer l’environnement avec tous les outils pré-intégrés. Tapez cette commande :

Bash
sudo docker build -t anos-custom:v1 .

### 3. Installer la commande globale (Optionnel mais recommandé)
Pour pouvoir lancer le système rapidement depuis n’importe quel dossier :

Bash
chmod +x anos
sudo cp anos /usr/local/bin/anos

### 4. Lancer le système d’exploitation ANOS
Une fois l’installation terminée, tapez simplement votre commande magique :

Bash
anos
(Ou exécutez directement le script Python si vous ne l’avez pas installé globalement : python3 lancer_bulle.py)

### 5. Utilisation à l’intérieur de la bulle
Pour vous anonymiser : tapez tor

Pour quitter le système : tapez exit
