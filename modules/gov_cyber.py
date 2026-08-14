import os
import subprocess

def ouvrir_dans_dock(cmd_docker):
    if "TMUX" in os.environ:
        try:
            nbr_panneaux = int(subprocess.check_output(["tmux", "display-message", "-p", "#{window_panes}"]).decode().strip())
            if nbr_panneaux == 1:
                subprocess.run(["tmux", "split-window", "-h", "-p", "45", cmd_docker])
            else:
                subprocess.run(["tmux", "select-pane", "-t", "{right}"])
                subprocess.run(["tmux", "split-window", "-v", cmd_docker])
            subprocess.run(["tmux", "select-pane", "-t", ".0"])
        except Exception:
            subprocess.run(cmd_docker, shell=True)
    else:
        subprocess.run(cmd_docker, shell=True)


def installer_pack_outils_cyber(nom_zone):
    print("\n[*] Lancement de l'installation de la Suite Cyber à droite...")
    cmd = (
        f"docker exec -it {nom_zone} sh -c '"
        f"rm -f /lib/apk/db/lock /var/cache/apk/*; "
        f"echo \"http://dl-cdn.alpinelinux.org/alpine/latest-stable/community\" >> /etc/apk/repositories 2>/dev/null; "
        f"apk update && "
        f"apk add --no-cache nmap tshark macchanger htop tor curl git python3 py3-pip exiftool poppler-utils ffmpeg w3m yt-dlp py3-gobject3 py3-cairo && "
        f"curl -sL https://raw.githubusercontent.com/jarun/ddgr/master/ddgr -o /usr/bin/ddgr && chmod +x /usr/bin/ddgr && "
        f"pip install --break-system-packages --no-deps mat2 binwalk && "
        f"echo -e \"\\n\\033[32m[✓] SUITE CYBER & OSINT INSTALLÉE AVEC SUCCÈS !\\033[0m\"; "
        f"read -p \"Appuyez sur Entrée pour fermer ce volet...\"'"
    )
    ouvrir_dans_dock(cmd)


def lancer_recherche_osint(nom_zone):
    pseudo = input("\n[?] Entrez le terme / pseudo à rechercher : ").strip()
    if not pseudo:
        return
    cmd = (
        f"docker exec -it {nom_zone} sh -c '"
        f"[ -f /usr/bin/ddgr ] || (curl -sL https://raw.githubusercontent.com/jarun/ddgr/master/ddgr -o /usr/bin/ddgr && chmod +x /usr/bin/ddgr); "
        f"/usr/bin/ddgr --np {pseudo}; "
        f"read -p \"Appuyez sur Entrée pour fermer...\"'"
    )
    ouvrir_dans_dock(cmd)


def telecharger_media_video(nom_zone):
    url = input("\n[?] Entrez l'URL du média/vidéo : ").strip()
    if not url:
        return
    cmd = f"docker exec -it {nom_zone} sh -c 'yt-dlp {url}; read -p \"Appuyez sur Entrée pour fermer...\"'"
    ouvrir_dans_dock(cmd)


def lancer_navigateur_securise(nom_zone):
    url = input("\n[?] URL (défaut: html.duckduckgo.com) : ").strip() or "https://html.duckduckgo.com"
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    cmd = f"docker exec -it {nom_zone} w3m '{url}'"
    ouvrir_dans_dock(cmd)
