from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = '🛍️ Store Management'

    def ready(self):
        import products.signals
