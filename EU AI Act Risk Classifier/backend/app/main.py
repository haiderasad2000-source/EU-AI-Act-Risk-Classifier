from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import classify

app = FastAPI(title="EU AI Act Risk Classifier", version="5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classify.router)

@app.get("/")
async def root():
    return {"message": "EU AI Act Risk Classifier API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
