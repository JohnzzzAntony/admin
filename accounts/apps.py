from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = '🔐 User Management'

    def ready(self):
        # Import signals to register them
        import accounts.signals
