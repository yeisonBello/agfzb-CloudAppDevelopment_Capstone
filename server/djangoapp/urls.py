from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
 

    path(route='', view=views.get_dealerships, name='index'),
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),
    path(route='dealer/<int:dealer_id>/post_review', view=views.add_review, name='post_review'),
  
    path('registration/', views.registration_request, name='registration'),
    path('about/', views.about_view, name='about'),
    path('contact/', view=views.contact, name='contact'),
    path('login/', views.login_request, name='login_request'),
    path('logout/', views.logout_request, name='logout'),
        
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)