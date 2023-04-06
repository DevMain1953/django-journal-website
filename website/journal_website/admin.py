from django.contrib import admin
from .models import String
from .models import StaticPage
from .models import ScientificPublication
from .models import Volume
from .models import ScientificSpecialty
from .models import Category
from .models import Founder
from .models import User
from .models import Article
from .models import Feedback

admin.site.register(String)
admin.site.register(StaticPage)
admin.site.register(ScientificPublication)
admin.site.register(Volume)
admin.site.register(ScientificSpecialty)
admin.site.register(Category)
admin.site.register(Founder)
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Feedback)
