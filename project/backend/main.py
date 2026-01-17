from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import patients, symptoms, predictions, appointments, consultations, voice, evaluation

app = FastAPI(
    title="Orthopaedic Expert System API",
    description="NLP-based appointment prioritization system for orthopaedic clinics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(symptoms.router)
app.include_router(predictions.router)
app.include_router(appointments.router)
app.include_router(consultations.router)
app.include_router(voice.router)
app.include_router(evaluation.router)


@app.get("/")
async def root():
    return {
        "message": "Orthopaedic Expert System API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "patients": "/patients",
            "symptoms": "/symptoms",
            "predictions": "/predictions",
            "appointments": "/appointments",
            "consultations": "/consultations",
            "voice": "/voice",
            "evaluation": "/evaluation",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orthopaedic-expert-system"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
