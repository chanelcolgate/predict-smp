from fastapi import FastAPI

# from src.routers.posts import router as posts_router
# from src.routers.users import router as users_router
from src.routers.models import router as models_router
from src.routers.smps import router as smps_router
from src.routers.revenues import router as revenues_router
from src.routers.offers import router as offers_router

app = FastAPI()

# app.include_router(posts_router, prefix='/posts', tags=['posts'])
# app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(models_router, prefix='/models', tags=['models'])
app.include_router(smps_router, prefix='/smps', tags=['smps'])
app.include_router(revenues_router, prefix='/revenues', tags=['revenues'])
app.include_router(offers_router, prefix='/offers', tags=['offers'])