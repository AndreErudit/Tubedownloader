from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import validators
import os

app = Flask(__name__)

# Crée le dossier downloads si pas existant
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    video = None
    message = ""

    if request.method == "POST":
        url = request.form.get("url")

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

    if not validators.url(url):
        return "Lien invalide !"

    try:
        # Définir options yt-dlp selon qualité
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': True
        }

        if quality == "mp3":
            ydl_opts.update({
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': '/usr/bin/ffmpeg'  # Render / Linux
            })
        elif quality == "720":
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
        elif quality == "1080":
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'
        else:
            ydl_opts['format'] = 'best'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)
            # Si MP3, changer extension
            if quality == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"

        # Retourner le fichier pour téléchargement dans le navigateur
        return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

    except Exception as e:
        return f"Erreur lors du téléchargement : {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))