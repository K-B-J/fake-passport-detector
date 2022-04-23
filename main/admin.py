from django.contrib import admin
from .models import *

admin.site.register(Issuer)
admin.site.register(Verifier)
admin.site.register(Security)
admin.site.register(Airports)
admin.site.register(FakePassportReport)
