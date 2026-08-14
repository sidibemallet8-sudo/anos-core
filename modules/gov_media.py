#!/usr/bin/env python3
"""
===============================================================================
  MODULE MULTIMÉDIA & NAVIGATEUR TEXTE - ANOS OS
===============================================================================
"""
import subprocess

def telecharger_media(nom_zone):
    """Télécharge une vidéo ou un média avec yt-dlp dans /documents."""
    url = input("\n[?] Colle l'URL de la vidéo/média à télécharger : ").strip()
    if url:
        cmd = f"apk add --no-cache yt-dlp 2>/dev/null && yt-dlp -P /documents '{url}'"
        subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", cmd])
    input("\nAppuyez sur Entrée...")

def lancer_browsh(nom_zone):
    """Lance Browsh (navigateur web dans le terminal)."""
    print("\n[*] Lancement de Browsh...")
    cmd = "apk add --no-cache browsh 2>/dev/null; browsh"
    subprocess.run(["docker", "exec", "-it", nom_zone, "sh", "-c", cmd])
