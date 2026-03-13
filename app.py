from flask import Flask, render_template, request, redirect, url_for
import yt_dlp
import validators
import os

app = Flask(__name__)

# Crée le dossier downloads si n'existe pas
if not os.path.exists('downloads'):
    os.makedirs('downloads')


@app.route("/", methods=["GET", "POST"])
def home():
    video = None
    message = ""

    if request.method == "POST":
        url = request.form.get("url")

        # Vérifie que le lien est valide
        if not validators.url(url):
            message = "Lien invalide !"
            return render_template("index.html", video=video, message=message)

        ydl_opts = {'quiet': True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video = {
                    "title": info.get("title"),
                    "thumbnail": info.get("thumbnail"),
                    "url": url
                }
        except Exception as e:
            message = f"Erreur lors de l'analyse : {str(e)}"

    return render_template("index.html", video=video, message=message)


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    quality = request.form.get("quality")
    message = ""

    if not validators.url(url):
        message = "Lien invalide !"
        return render_template("index.html", video=None, message=message)

    # Configuration yt-dlp pour chaque qualité
    if quality == "mp3":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg',  # chemin FFmpeg Render
            'quiet': True
        }
    elif quality == "720":
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }
    elif quality == "1080":
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }
    else:
        # Défaut : meilleure qualité
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        message = "Téléchargement terminé !"
    except Exception as e:
        message = f"Erreur lors du téléchargement : {str(e)}"

    # Après téléchargement, retourne sur page d'accueil
    return render_template("index.html", video=None, message=message)


if __name__ == "__main__":
    # NE PAS mettre debug=True sur Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))