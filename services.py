import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database, models as _models, schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_username(username: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.username == username).first()

async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        username=user.username, email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(username: str, password: str, db: _orm.Session):
    user = await get_user_by_username(db=db, username=username)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)

async def create_userProfile(user: _models.User, db: _orm.Session):
    profile = _models.UserProfile(owner_username=user.username, owner_email=user.email)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    print("PROFILE IS CREATED SUCCESSFULLY")
    return _schemas.UserProfile.from_orm(profile)

async def get_userProfile(user: _models.User, db: _orm.Session):
    profile = db.query(_models.UserProfile).filter(_models.UserProfile.owner_username == user.username).first()
    return _schemas.UserProfile.from_orm(profile)

async def update_profile(profile: _schemas.UserProfileCreate, user: _models.User, db: _orm.Session):
    profile_db = db.query(_models.UserProfile).filter(_models.UserProfile.owner_username == user.username).first()

    profile_db.location = profile.location
    profile_db.status1 = profile.status1
    profile_db.status2 = profile.status2
    profile_db.name = profile.name
    profile_db.surname = profile.surname
    profile_db.nickname = profile.nickname
    profile_db.phone = profile.phone
    profile_db.gender = profile.gender
    profile_db.birth = profile.birth
    db.commit()
    db.refresh(profile_db)

    return _schemas.UserProfile.from_orm(profile_db)

async def create_recipe(user: _schemas.User, db: _orm.Session, recipe: _schemas.RecipeCreate):
    recipe = _models.Recipe(**recipe.dict(), owner_username=user.username)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return _schemas.Recipe.from_orm(recipe)

async def get_recipes(user: _schemas.User, db: _orm.Session):
    recipes = db.query(_models.Recipe).filter_by(owner_username=user.username)

    return list(map(_schemas.Recipe.from_orm, recipes))

async def _recipe_selector(recipe_id: int, user: _schemas.User, db: _orm.Session):
    recipe = (
        db.query(_models.Recipe)
        .filter_by(owner_username=user.username)
        .filter(_models.Recipe.recipe_id == recipe_id)
        .first()
    )

    if recipe is None:
        raise _fastapi.HTTPException(status_code=404, detail="Recipe does not exist")

    return recipe

async def get_recipe(recipe_id: int, user: _schemas.User, db: _orm.Session):
    recipe = await _recipe_selector(recipe_id=recipe_id, user=user, db=db)

    return _schemas.Recipe.from_orm(recipe)

async def delete_recipe(recipe_id: int, user: _schemas.User, db: _orm.Session):
    recipe = await _recipe_selector(recipe_id, user, db)

    db.delete(recipe)
    db.commit()

async def update_recipe(recipe_id: int, recipe: _schemas.RecipeCreate, user: _schemas.User, db: _orm.Session):
    recipe_db = await _recipe_selector(recipe_id, user, db)

    recipe_db.recipe_name = recipe.recipe_name
    recipe_db.ingredients = recipe.ingredients
    recipe_db.steps = recipe.steps
    db.commit()
    db.refresh(recipe_db)

    return _schemas.Recipe.from_orm(recipe_db)


async def get_all_recipes(db: _orm.Session):
    pass