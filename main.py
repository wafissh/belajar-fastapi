from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException 
from fastapi.responses import JSONResponse
from schemas import *
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import Base, engine, create_engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")





@app.get("/", name="home", include_in_schema=False)
@app.get("/posts", name="posts", include_in_schema=False)
def home(request: Request, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(request, "home.html", {"posts" : posts, "title" : "Home Page"})

@app.get("/posts/{post_id}", name="post", include_in_schema=False)
def get_post(request: Request, post_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post":post, "title": post.title[:50]}
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")

@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )




#----------------- API ------------------

@app.get("/api/posts", response_model=list[ResponsePost])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

@app.get("/api/posts/{post_id}", response_model=ResponsePost)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_exist = result.scalars().first()
    if user_exist:
        return user_exist

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

@app.get("/api/users/{user_id}/posts", response_model=list[ResponsePost])
def get_user_posts(user_id:int, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user_exist = result.scalars().first()
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    result_post = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result_post.scalars().all()
    if posts:
        return posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")



#-------------------------- API POST -----------------
@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user:UserCreate, db:Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"User with {user.username} already exist"
        )
    result_email = db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_email = result_email.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Email with {user.email} already exist"
        )
    
    new_user = models.User(
        username = user.username,
        email = user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post(
    "/api/posts",
    response_model=ResponsePost,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: CreatePost, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post






#-------------------- ERROR HANDLING----------------


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )

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



    
