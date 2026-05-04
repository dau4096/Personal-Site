"main.py"
import flask;
import markdown as md;
import frontmatter as fm;
import ffmpeg;
import os;
import hashlib;
from pathlib import Path;


app = flask.Flask(__name__);


PAGES_DIR:str = "pages";
PROJECTS_DIR:str = "pages/projects";
GALLERY_DIR:str = "pages/gallery";
POSTS_DIR:str = "pages/posts";
MUSIC_DIR:str = "/home/dau/Music";



def loadMD(path:str) -> tuple[str, str]|None:
	if (not os.path.exists(path)): return None;
	with open(path, "r", encoding="utf-8") as f:
		post = fm.load(f);
	html = md.markdown(post.content, extensions=["fenced_code", "tables", "nl2br"]);
	return post.metadata, html



#General
@app.route("/")
def indexPage() -> str:
	pageMD = loadMD(f"{PAGES_DIR}/site.index.md");
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);


@app.route("/<pageName>/")
def genericPage(pageName:str) -> str:
	path:str = f"{PAGES_DIR}/{pageName}.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);




#Projects
@app.route("/projects/")
def projectIndex() -> str:
	path:str = f"{PAGES_DIR}/projects.index.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);


@app.route("/projects/<name>/")
def projectPage(name:str) -> str:
	path:str = f"{PROJECTS_DIR}/{name}.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);



#Gallery
@app.route("/gallery/")
def galleryIndex() -> str:
	path:str = f"{PAGES_DIR}/gallery.index.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);


@app.route("/gallery/<name>/")
def galleryPage(name:str) -> str:
	path:str = f"{GALLERY_DIR}/{name}.md";
	pageMD:str = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("gallery.html", meta=meta, content=content);



#Posts
@app.route("/posts/")
def postsIndex() -> str:
	path:str = f"{PAGES_DIR}/posts.index.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);


@app.route("/posts/<name>/")
def postPage(name:str) -> str:
	path:str = f"{POSTS_DIR}/{name}.md";
	pageMD:str = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);



#Audio
@app.route("/audio/")
def audioIndex() -> str:
	path:str = f"{PAGES_DIR}/audio.index.md";
	pageMD = loadMD(path);
	if (pageMD is None): flask.abort(404);

	(meta, content) = pageMD;
	return flask.render_template("default.html", meta=meta, content=content);


@app.route("/audio/<dir>/<name>/")
def audioPage(dir:str, name:str) -> str:
	file_path = f"/audio/file/{dir}/{name}.mp3";

	meta = {
		"title": name,
		"description": "Audio Playback",
		"image": "/static/embed.png"
	};

	return flask.render_template(
		"audio.html",
		meta=meta,
		file=file_path
	);


@app.route("/audio/file/<path:subpath>")
def audio(subpath):
	return flask.send_from_directory(
		os.path.expanduser("~/Music"),
		subpath
	);


@app.route("/audio/embed/<path:subpath>")
def audio_embed(subpath:str):
	base = Path(MUSIC_DIR).resolve();
	target = (base / subpath).resolve();

	if (not str(target).startswith(str(base))):
	    abort(403);

	image = ffmpeg.input("static/audioEmbed.png", loop=1);
	audio = ffmpeg.input(f"{MUSIC_DIR}/{subpath}");

	fileHash = hashlib.md5(f"{subpath}".encode()).hexdigest()
	out:str = f"/home/dau/Videos/cache/{fileHash}.mp4";

	if (not os.path.exists(out)):
		#Create the cached version.
		ffmpeg.output(
		    image, audio, out,
		    vcodec='libx264',
		    preset='ultrafast',
		    s='128x128',
		    pix_fmt='yuv420p',
		    tune='stillimage',
		    acodec='aac',
		    shortest=None
		).run(overwrite_output=True);
	return flask.send_from_directory(
		os.path.expanduser("~/Videos/cache"),
		f"{fileHash}.mp4"
	);


#Video
@app.route("/video/file/<path:subpath>")
def video(subpath):
	return flask.send_from_directory(
		os.path.expanduser("~/Videos/share"),
		subpath
	);





if (__name__ == "__main__"):
	app.run(host="0.0.0.0", port=5000, debug=True);
