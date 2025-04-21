from django.apps import AppConfig
from django.conf import settings
import os
import pickle

class ReviewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"


    path = os.path.join(settings.MODELS, 'models.p')

    with open(path, 'rb') as file:
        data = pickle.load(file)
    model= data['model']
    vectorizer = data['vectorizer']
