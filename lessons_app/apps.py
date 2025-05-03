from django.apps import AppConfig


class LessonsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lessons_app'

    def ready(self):
        import lessons_app.signals  # Signalni faollashtirish




