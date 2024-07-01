# webproj/app/apps.py

import os
from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if os.environ.get('RUN_SPARQL_QUERIES', 'true') == 'true':
            from .triplestore.inferences import infer_queries
            infer_queries()
