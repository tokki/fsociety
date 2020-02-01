from django.contrib import admin

# Register your models here.
from .models import Movie, Seed

admin.site.register(Movie)
admin.site.register(Seed)
