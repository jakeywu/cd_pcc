import uvicorn
from app.src.settings.c_logger import LOG_CONFIGURE
from app.src.routers.pcc import pcc_router
from app.src.initial import env
from fastapi import FastAPI


APP = FastAPI()


if __name__ == "__main__":
    APP.include_router(pcc_router)
    uvicorn.run(
        app=APP,
        host=env.server.SERVER_HOST,
        port=env.server.SERVER_PORT,
        log_config=LOG_CONFIGURE
    )

