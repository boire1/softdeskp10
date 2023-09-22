"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_app.views import profile
from softdesk.views import home
from django.contrib.auth.views import LogoutView

# ... (les autres routers pour les autres apps)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include('user_app.urls')),  # Ici, on inclut les URLs de user_app
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('api/', include('proj_contrib_app.urls')),
    path('api/', include('issue_com_app.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
