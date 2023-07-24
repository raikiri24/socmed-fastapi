from fastapi import APIRouter
from models import all_models
from configs.db import engine, SessionLocal, get_db
from fastapi import Depends, HTTPException, APIRouter
from .auth import get_current_user, get_user_exception
from sqlalchemy.orm import Session
from schemas.posts import Post
import datetime
import pytz
import json

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)

all_models.Base.metadata.create_all(bind=engine)


@router.get("/users")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return {"message": db.query(all_models.Posts)
            .filter(all_models.Posts.owner_id == user.get("id"), all_models.Posts.deleted_date.is_(None))
            .all()}


@router.post("/")
async def create_post(post: Post,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    post_model = all_models.Posts()
    post_model.title = post.title
    post_model.description = post.description
    post_model.owner_id = user.get("id")

    db.add(post_model)
    db.commit()

    post_obj_ret = {"id": post_model.id}
    return successful_response(201, message=json.dumps(post_obj_ret))


@router.put("/{post_id}")
async def update_post(post_id: int,
                      post: Post,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    post_model = db.query(all_models.Posts)\
        .filter(all_models.Posts.id == post_id)\
        .filter(all_models.Posts.owner_id == user.get("id"))\
        .first()

    if post_model is None:
        raise http_exception()

    post_model.title = post.title
    post_model.description = post.description

    db.add(post_model)
    db.commit()

    return successful_response(200)


@router.put("/soft_delete/{post_id}")
async def update_post(post_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    post_model = db.query(all_models.Posts)\
        .filter(all_models.Posts.id == post_id)\
        .filter(all_models.Posts.owner_id == user.get("id"))\
        .first()

    if post_model is None:
        raise http_exception()

    post_model.deleted_date = datetime_now()

    db.add(post_model)
    db.commit()

    return successful_response(200)


@router.delete("/{post_id}")
async def delete_post(post_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    post_model = db.query(all_models.Posts)\
        .filter(all_models.Posts.id == post_id)\
        .filter(all_models.Posts.owner_id == user.get("id"))\
        .first()

    if post_model is None:
        raise http_exception()

    db.query(all_models.Posts)\
        .filter(all_models.Posts.id == post_id)\
        .delete()

    db.commit()

    return successful_response(200)


def datetime_now():
    timezone = pytz.timezone('Asia/Manila')

    ph_date_time = datetime.datetime.now(timezone)
    return ph_date_time


def successful_response(status_code: int, message=None):
    return {
        'status': status_code,
        'transaction': 'Successful',
        'message': message
    }


def http_exception():
    return HTTPException(status_code=404, detail="Post not found")
