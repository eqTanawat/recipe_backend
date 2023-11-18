import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True, index=True)
    email = _sql.Column(_sql.String, index=True)
    hashed_password = _sql.Column(_sql.String)

    # profile_username = _orm.relationship("UserProfile", back_populates="owner_username_")
    # profile_email = _orm.relationship("UserProfile", back_populates="owner_email_")

    recipes = _orm.relationship("Recipe", back_populates="owner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    

class UserProfile(_database.Base):
    __tablename__ = "userprofiles"
    owner_username = _sql.Column(_sql.String, _sql.ForeignKey("users.username"), primary_key=True)
    owner_email = _sql.Column(_sql.String, _sql.ForeignKey("users.email"))
    location = _sql.Column(_sql.String, index=True, default="")
    status1 = _sql.Column(_sql.String, index=True, default="")
    status2 = _sql.Column(_sql.String, index=True, default="")
    name = _sql.Column(_sql.String, index=True, default="")
    surname = _sql.Column(_sql.String, index=True, default="")
    nickname = _sql.Column(_sql.String, index=True, default="")
    phone = _sql.Column(_sql.String, index=True, default="")
    gender = _sql.Column(_sql.String, index=True, default="")
    birth = _sql.Column(_sql.String, index=True, default="")
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    username_relation = _orm.relationship("User", foreign_keys=[owner_username])
    email_relation = _orm.relationship("User", foreign_keys=[owner_email])


class Recipe(_database.Base):
    __tablename__ = "recipes"
    recipe_id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_username = _sql.Column(_sql.String, _sql.ForeignKey("users.username"))
    recipe_name = _sql.Column(_sql.String, index=True)
    ingredients = _sql.Column(_sql.String, index=True)
    steps = _sql.Column(_sql.String, index=True)
    # images = _sql.Column(_sql.String, index=True)

    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="recipes")


# class Post(_database.Base):
#     __tablename__ = "posts"
#     recipe_id = _sql.Column(_sql.Integer,  _sql.ForeignKey("recipes.recipe_id"), primary_key=True, index=True)
#     reviews_id = _sql.Column(_sql.Integer, index=True)

# class Review(_database.Base):
#     __tablename__ = "reviews"
#     review_id = _sql.Column(_sql.Integer, index=True)
#     rating = _sql.Column(_sql.Integer, index=True)
#     comment = _sql.Column(_sql.String, index=True)
#     reveiwer = _sql.Column(_sql.String, index=True)