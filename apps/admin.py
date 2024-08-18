from django.contrib import admin
from .models import App

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
  list_display = ("name", "uploaded_by")
  prepopulated_fields = {"slug": ("name", "uploaded_by")}

admin.site.register(App, MemberAdmin)