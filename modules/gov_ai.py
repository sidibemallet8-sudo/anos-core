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


def installer_moteurs_ia(nom_zone):
    print("\n[*] Lancement de l'installation des moteurs IA & OCR à droite...")
    cmd = (
        f"docker exec -it {nom_zone} sh -c '"
        f"rm -f /lib/apk/db/lock; "
        f"echo \"http://dl-cdn.alpinelinux.org/alpine/latest-stable/community\" >> /etc/apk/repositories 2>/dev/null; "
        f"apk update && "
        f"apk add --no-cache tesseract-ocr tesseract-ocr-data-fra poppler-utils && "
        f"echo -e \"\\n\\033[32m[✓] MOTEURS IA & OCR INSTALLÉS AVEC SUCCÈS !\\033[0m\"; "
        f"read -p \"Appuyez sur Entrée pour fermer ce volet...\"'"
    )
    ouvrir_dans_dock(cmd)
