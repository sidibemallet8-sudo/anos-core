#!/bin/bash

VERT='\033[1;32m'
BLEU='\033[1;34m'
NEUTRE='\033[0m'

echo -e "${BLEU}====================================================${NEUTRE}"
echo -e "${VERT}    ANOS ENVIRONMENT - AUTOMATIC INSTALLER (IA)    ${NEUTRE}"
echo -e "${BLEU}====================================================${NEUTRE}"

echo -e "\n${VERT}[*] Mise à jour des paquets système et prérequis...${NEUTRE}"
sudo apt update && sudo apt install -y curl git python3-pip python3-venv

echo -e "\n${VERT}[*] Vérification / Installation d'Ollama...${NEUTRE}"
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo -e "[+] Ollama est déjà installé."
fi

echo -e "\n${VERT}[*] Téléchargement du modèle IA (qwen2.5-coder:1.5b)...${NEUTRE}"
ollama pull qwen2.5-coder:1.5b

echo -e "\n${VERT}[*] Installation et déploiement de PentestGPT...${NEUTRE}"
if [ ! -d "PentestGPT" ]; then
    # Lien officiel corrigé (GreyDGL)
    git clone https://github.com/GreyDGL/PentestGPT.git
    cd PentestGPT
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install . --break-system-packages
    cd ..
    echo -e "[+] PentestGPT installé avec succès."
else
    echo -e "[+] PentestGPT est déjà présent."
fi

echo -e "\n${BLEU}====================================================${NEUTRE}"
echo -e "${VERT}[+] CONFIGURATION TERMINÉE AVEC SUCCÈS !${NEUTRE}"
echo -e "${VERT}[+] Pour lancer ANOS : python3 lancer_bulle.py${NEUTRE}"
echo -e "${BLEU}====================================================${NEUTRE}"
