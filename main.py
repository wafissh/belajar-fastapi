from fastapi import FastAPI, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException 
from fastapi.responses import JSONResponse
from schemas import CreatePost, ResponsePost
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

@app.get("/post/{post_id}", name="post")
def get_post(request: Request, post_id:int):
    for p in post:
        if p.get("id") == post_id:
            title = p["title"][:50]
            return templates.TemplateResponse(request, "post.html", {"post": p, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")


@app.get("/api/posts", response_model=list[ResponsePost])
def get_post_api():
    return post


@app.get("/api/posts/{post_id}, response_model=ResponsePost")
def get_posts(post_id: int):
    for p in post:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(request, "404.html", {"status": status.HTTP_404_NOT_FOUND, "message":"HTTP Not Found "})

@app.exception_handler(RequestValidationError)
def validation_error_handler(request:Request, exception:RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"message": exception.errors()}
        )
    return templates.TemplateResponse(
        request,
        "404.html",
        {"status": status.HTTP_422_UNPROCESSABLE_CONTENT,
         "message": "Invalid Request"
        }

    )


@app.post(
    "/api/posts",
    response_model=ResponsePost,
    status_code=status.HTTP_201_CREATED
)
def create_post(post_model:CreatePost):
    new_id = max(p['id'] for p in post) + 1 if post else 1
    new_post = {
        "id":new_id,
        "author": post_model.author,
        "title": post_model.title,
        "content": post_model.content,
        "date_posted": "6 July, 2026",
    }
    post.append(new_post)
    return new_post
    
