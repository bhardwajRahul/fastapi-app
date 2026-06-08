import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_ALLOWED_ORIGINS = "*"
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS)


def setup(app: FastAPI):
    origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

    # credentials cannot be combined with a wildcard origin under the cors spec
    allow_credentials = origins != ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
