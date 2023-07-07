from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from config.config import config_by_name
from database import init_config as db_init_config
from apis.controller import internal_message_router, message_router


app = FastAPI()

#  ---------  INTERNAL API ----------------------------------------
app.include_router(internal_message_router,
                   prefix='/internal_api/v1/api_management/messages')

#  ---------  PUBLIC API REQUIRED AUTHENTICATION  -----------------
app.include_router(message_router, prefix='/api/v1/api_management/messages')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_config():
    config_name = os.getenv('SERVICE_ENV') or 'dev'
    config = config_by_name[config_name]
    return config


@app.on_event('startup')
async def startup_event():
    config = load_config()
    await db_init_config(config)
    # init logging
    # init tracing


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5000, reload=True)
