from fastapi import FastAPI

from helpers import cors, log, rate_limiter, router, static
from helpers.lifespan import lifespan

# log
log.setup()

# app
app = FastAPI(lifespan=lifespan)
rate_limiter.setup(app)
cors.setup(app)

# routes
router.setup(app)
static.setup(app)

# scheduled jobs
import jobs.my_model  # noqa: F401
