from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

video_info = {}

@app.route("/", methods=["GET","POST"])
def home():

    global video_info

    if request.method == "POST":

        url = request.form["url"]

        ydl_opts = {}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            video_info = {
                "title": info["title"],
                "thumbnail": info["thumbnail"],
                "url": url
            }

        return render_template("index.html", video=video_info)

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():

    format = request.form["format"]
    url = video_info["url"]

    if format == "mp3":

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

    elif format == "720":

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

    else:

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "Téléchargement terminé"

if __name__ == "__main__":
    app.run(debug=True)