from typing import List
import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm

import services as _services, schemas as _schemas

app = _fastapi.FastAPI()


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_username(user.username, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="username already in use")

    user = await _services.create_user(user, db)
    profile = await _services.create_userProfile(user, db)
    return await _services.create_token(user)

@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

# @app.post("/api/userprofile", response_model=_schemas.UserProfile)
# async def create_userProfile(
#     profile: _schemas.UserProfileCreate,
#     user: _schemas.User = _fastapi.Depends(_services.get_current_user),
#     db: _orm.Session = _fastapi.Depends(_services.get_db)
# ):
#     return await _services.create_userProfile(user=user, db=db, profile=profile)

@app.get("/api/userprofile/me", response_model=_schemas.UserProfile)
async def get_userProfile(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_userProfile(user=user, db=db)

@app.put("/api/userprofile/me", status_code=200)
async def update_profile(
    profile: _schemas.UserProfileCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_profile(profile, user, db)
    return {"message" : "Profile updated"}

@app.post("/api/recipes", response_model=_schemas.Recipe)
async def create_recipe(
    recipe: _schemas.RecipeCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_recipe(user=user, db=db, recipe=recipe)

@app.get("/api/recipes", response_model=List[_schemas.Recipe])
async def get_recipes(
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_recipes(user=user, db=db)

@app.get("/api/recipes/{recipe_id}", status_code=200)
async def get_recipe(
    recipe_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_recipe(recipe_id, user, db)

@app.delete("/api/recipes/{recipe_id}", status_code=204)
async def delete_recipe(
    recipe_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_recipe(recipe_id, user, db)
    return {"message", "Successfully Deleted"}

@app.put("/api/recipes/{recipe_id}", status_code=200)
async def update_recipe(
    recipe_id: int,
    recipe: _schemas.RecipeCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_recipe(recipe_id, recipe, user, db)
    return {"message" : "Successfully Updated"}


@app.get("/recipes")
async def recipes(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    pass


@app.get("/api")
async def root():
    return {"message": "Awesome Leads Manager"}


@app.get("/")
async def show():
    return {"message": "This is the hompage"}