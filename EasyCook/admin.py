from django.contrib import admin


from .models import Frigo
admin.site.register(Frigo)

from .models import Photo_plat
admin.site.register(Photo_plat)

from .models import Recette
admin.site.register(Recette)

from .models import Review
admin.site.register(Review)

from .models import Service
admin.site.register(Service)

from .models import Ingredients
admin.site.register(Ingredients)

from .models import SiteLanguage
admin.site.register(SiteLanguage)