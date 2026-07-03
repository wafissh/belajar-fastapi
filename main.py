from fastapi import FastAPI, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
post = [{
    "id": 1,
    "author": "Corey Schafer",
    "title": "FastAPI is Awesome",
    "content": "This framework is really easy to use and super fast.",
    "date_posted": "April 20, 2025",
},
{
    "id": 2,
    "author": "Jane Doe",
    "title": "Python is Great for Web Development",
    "content": "Python is a great language for web development, and FastAPI makes it even...",
    "date_posted": "April 21, 2025",
},]


@app.get("/", name="home")
@app.get("/posts", name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts" : post, "title" : "Home Page"})

@app.get("/post/{post_id}")
def get_post(request: Request, post_id:int):
    for p in post:
        if p.get("id") == post_id:
            title = p["title"][:50]
            return templates.TemplateResponse(request, "post.html", {"post": p, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")



@app.get("/api/posts/{post_id}")
def get_posts(post_id: int):
    for p in post:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, "404.html")