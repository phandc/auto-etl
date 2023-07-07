import os
import urllib
import logging


class Config:
    LOG_LEVEL = logging.INFO
    NAME = 'api-management-service'
    TOKEN = ''


class DevelopmentConfig(Config):
    MONGO_URI = f'mongodb://root:example@mongo:27017/'


config_by_name = dict(
    dev=DevelopmentConfig,
)
