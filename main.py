from fastapi import FastAPI
import uvicorn
from actions import user_tracker, event_tracker, contribution_tracker, analytics_tracker

app = FastAPI(
    title="Contribution Tracker API",
    description="REST API service providing access to User, Event, and Contribution operations with Swagger UI documentation.",
    version="1.0.0"
)

app.include_router(user_tracker.router)
app.include_router(event_tracker.router)
app.include_router(contribution_tracker.router)
app.include_router(analytics_tracker.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Contribution Tracker API",
        "swagger_docs": "/docs",
        "redoc_docs": "/redoc"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)