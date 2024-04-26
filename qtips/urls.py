from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from Authenticationapp import views
from Authenticationapp import views
from django.conf.urls import handler400,handler500,handler404,handler403
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/',views.logout_req,name="logout" ),
    path('',include('CART.urls')),
    path('',include('Ecommerceapp.urls')),
    #  path('',include('wishlist.urls')),
    path('auth/',include('Authenticationapp.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#Django Administration apperarence edit
admin.site.site_header = "QTipstore Administration"
admin.site.site_title = "QTipstore Admin Portal"
admin.site.index_title = "Welcome to QTipstore Researcher Portal"