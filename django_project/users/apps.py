from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users' # Setting the name of class UsersConfig to "users"

    def ready(self) :
        import users.signals

# ensures signals are registered on startup