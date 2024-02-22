from django.urls import path,include
from c2g.views import *
urlpatterns = [
    path('',home_view,name='home'),
    path('convert/',getting,name="input veiw"),
    path('apierror/',apierror,name="apierror"),
]