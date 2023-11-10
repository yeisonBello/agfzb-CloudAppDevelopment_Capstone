from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
 

    path(route='', view=views.get_dealerships_state, name='index'),# funciona todo 
    #path('<str:state>/', view=views.get_dealerships_state, name='index'), # hay un problema aqui que no deja cargar las otras
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),# funciona a la mitad
    
    
   
    path(route='dealer/<int:dealer_id>/add_review', view=views.add_review, name='add_review'),
  
 

   
    path('registration/', views.registration_request, name='registration'),
    path('about/', views.about_view, name='about'),
    path('contact/', view=views.contact, name='contact'),
    path('login/', views.login_request, name='login_request'),
    path('logout/', views.logout_request, name='logout'),
        
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)