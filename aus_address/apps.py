from django.apps import AppConfig

class AusAddressConfig(AppConfig):
    name = 'aus_address'  
    
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "Australian Addresses"
    
    def ready(self):
        pass    