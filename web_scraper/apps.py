from django.apps import AppConfig
from .views import *
import time

class WebScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_scraper'
    run_scraper_code()


