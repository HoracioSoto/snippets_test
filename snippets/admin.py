from django.contrib import admin

from .models import Language, Snippet


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Language model.
    """
    list_display = (
        "name",
        "slug",
    )

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    """
    Admin interface for the Snippet model.
    """
    list_display = (
        "user",
        "name",
        "language",
        "snippet",
        "public"
    )
