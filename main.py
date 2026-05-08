"main.py"
import flask;
import markdown as md;
import frontmatter as fm;
import ffmpeg;
import os;
import hashlib;
from pathlib import Path;
from mutagen import File as MutagenFile;


app = flask.Flask(__name__);


PAGES_DIR:str = "pages";
PROJECTS_DIR:str = "pages/projects";
GALLERY_DIR:str = "pages/gallery";
POSTS_DIR:str = "pages/posts";
MUSIC_DIR:str = Path("~/Music").expanduser().resolve();


AUDIO_DIR_MAP:dict[str, str] = {
	"d4": "DFour",
	"escala": "Escala",
	"exa": "Exapunks OST",
	"ez2": "Entropy:Zero 2 OST",
	"fd": "Frontier Defense OST", "mp3": ".MP3", "wav": ".WAV",
	"hl": "Half-Life OST", "extern": "Extra",
	"keygen": "Keygen Church",
	"kf": "Killing Floor OST",
	"kingslayer": "Kingslayer",
	"mediaeval": "Bardcore",
	"mirror": "Mirror's Edge OST",
	"other": "Miscellaneous", "mp4": ".MP4",
	"powerpoint": "\"Music to listen to when doing your Powerpoint homework\"",
	"tomb": "The Living Tombstone",
	"vocaloid": "Vocaloid",
	"waitin": "SAM WAITIN",

	#All of the UK subfolders
	"ultrakill": "ULTRAKILL OST",
	"7-E": "VIOLENCE /// ENCORE [UST]",
	"azure": "AzureNova", "richaadeb": "RichaadEB", "rex": "Rex Shreddington",
	"fuck.you": "Miscellaneous",
	"official-ogg": ".OGG",
	"_.miscellaneous": "Miscellaneous", "_.museum": "Museum","0.prelude": "0: Prelude",
	"1.limbo": "1: Limbo", "2.lust": "2: Lust", "3.gluttony": "3: Gluttony",
	"4.greed": "4: Greed", "5.wrath": "5: Wrath", "6.heresy": "6: Heresy",
	"7.violence": "7: Violence", "8.fraud": "8: Fraud", "9.treachery": "9: Treachery"
};



#Helpers
def loadMD(path:str) -> tuple[str, str]|None:
	if (not os.path.exists(path)): return None;
	with open(path, "r", encoding="utf-8") as f:
		post = fm.load(f);
	html = md.markdown(post.content, extensions=["fenced_code", "tables", "nl2br"]);
	return post.metadata, html

def loadHTML(path:str) -> str:
	if (not os.path.exists(path)): return "";

	html:str = "";
	with open(path, "r", encoding="utf-8") as f:
		html = fm.load(f);

	return html.content;


def getMP3meta(path):
	try:
		audio = MutagenFile(path);
		if (audio is None):
			return {};

		tags = audio.tags or {};

		def first(tagName:str, default:str=""):
			value = tags.get(tagName);
			if (value is None):
				return default;

			if (isinstance(value, list)):
				return str(value[0]);

			return str(value);

		return {
			"title": first("TIT2") or first("title") or path.stem,
			"artist": first("TPE1") or first("artist"),
			"album": first("TALB") or first("album"),
			"track": first("TRCK") or first("tracknumber"),
		};

	except Exception:
		return {};


def parseTrackID(track):
	if (not track):
		return 1e6;

	#Handle formats like "X/Y" (Where Y is total in album)
	track = str(track).split("/")[0];

	try:
		return int(track);
	except ValueError:
		return 1e6;





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
		MUSIC_DIR, subpath
	);


@app.route("/audio/index/")
@app.route("/audio/index/<path:subpath>")
def audioIndex(subpath:str=""):
	currentDir:Path = (MUSIC_DIR / subpath).resolve();

	#Prevent path traversal
	if (not str(currentDir).startswith(str(MUSIC_DIR))):
		flask.abort(403);

	#Does it exist
	if (not currentDir.exists()):
		flask.abort(404);

	entries:list[dict[str, str]] = [];

	for item in sorted(currentDir.iterdir()):
		relativePath:Path = item.relative_to(MUSIC_DIR);

		entry = {
			"name": item.name,
			"path": relativePath.as_posix(),
			"isDirectory": item.is_dir(),
		};

		if (item.is_file()):
			if (not (str(item).endswith(".mp3") or str(item).endswith(".wav") or str(item).endswith(".ogg"))): continue;
			meta = getMP3meta(item)

			entry["title"] = meta.get("title", item.stem);
			entry["artist"] = meta.get("artist", "");
			entry["album"] = meta.get("album", "");
			entry["track"] = meta.get("track", "");

			entry["track_num"] = parseTrackID(entry["track"]);

		elif (entry["name"] in AUDIO_DIR_MAP): entry["name"] = AUDIO_DIR_MAP[entry["name"]];

		entries.append(entry);


	entries.sort(
		key=lambda e: (
			not e["isDirectory"],
			e.get("track_num", 1e6),
			e["name"].lower()
		)
	)
	


	parent = None;
	if (currentDir != MUSIC_DIR):
		parent = currentDir.parent.relative_to(MUSIC_DIR).as_posix();

	return flask.render_template_string(loadHTML("templates/audio-index.html"), entries=entries, parent=parent)


@app.route("/audio/download/<path:subpath>")
def audio_download(subpath):
	return flask.send_from_directory(
		MUSIC_DIR, subpath, as_attachment=True
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
