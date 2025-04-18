import uvicorn
from app.src.settings.c_logger import LOG_CONFIGURE
from app.src.routers.pcc import pcc_router
from app.src.initial import env
from fastapi import FastAPI
import threading
import logging

from app.src.subscriber import sub_main  # 假设你将订阅逻辑放这里

APP = FastAPI()

def start_subscriber():
    logging.info("启动 Redis 订阅线程")
    sub_main()

if __name__ == "__main__":
    APP.include_router(pcc_router)

    # 启动 Redis 订阅线程
    subscriber_thread = threading.Thread(target=start_subscriber, daemon=True)
    subscriber_thread.start()

    uvicorn.run(
        app=APP,
        host=env.server.SERVER_HOST,
        port=env.server.SERVER_PORT,
        log_config=LOG_CONFIGURE
    )
