from django.apps import AppConfig
from app.triplestore.inferences import infer_queries


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        infer_queries()
