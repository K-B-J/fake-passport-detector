from django.contrib import admin
from .models import *

admin.site.register(Issuer)
admin.site.register(Verifier)
admin.site.register(Security)
