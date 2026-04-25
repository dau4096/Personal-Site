"main.py"
import flask;
import markdown as md;
import frontmatter as fm;
import os;


app = flask.Flask(__name__);

PAGES_DIR:str = "pages";
PROJECTS_DIR:str = "pages/projects";
GALLERY_DIR:str = "pages/gallery";

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


if (__name__ == "__main__"):
    app.run(debug=True);