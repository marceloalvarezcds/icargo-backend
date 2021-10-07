import uvicorn  # type: ignore
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app import app
from app.config import REPORTS_FOLDER, settings
from app.dependencies import get_database_connection
from app.endpoints import api
from app.middlewares import AuditRequestMiddleware

app.mount("/reports", StaticFiles(directory=REPORTS_FOLDER), name=REPORTS_FOLDER)

app.add_middleware(
    AuditRequestMiddleware, database_connection_function=get_database_connection
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api)


# Run Server
if __name__ == "__main__":
    uvicorn.run(app, port=8101)
    # app.run(host="0.0.0.0", debug=True)
