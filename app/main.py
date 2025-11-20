from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.inventory import router as inventory_router
from app.api.v1.tickets import router as tickets_router
from app.api.v1.dashboard import router as dashboard_router   # ⬅️ new
from app.db.session import engine
from app.models import Base

app = FastAPI(title="Tailor Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev-friendly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(inventory_router, prefix="/api/v1")
app.include_router(tickets_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")   # ⬅️ new
