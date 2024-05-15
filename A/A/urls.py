
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls' , namespace='home')),
    path('accounts/', include('accounts.urls' , namespace='accounts')),
    path('orders/', include('orders.urls' , namespace='orders')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



###ina title haye tooye admin panel ro avaz mikonan

admin.site.site_header='myshop'
admin.site.site_title='ecommerce'
admin.site.index_title='welcome to ghazal`s shop'
