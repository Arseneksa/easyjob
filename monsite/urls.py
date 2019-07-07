"""monsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from EasyJob import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
app_name = 'easyjob'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('base/', views.base, name="base"),
    path('', views.index, name="home"),
    path('default', views.default, name="default"),
    path('home/<int:job_id>/', views.home2, name="accounthome"),
    path('home/', views.home, name="accounthome"),
    path('account/profil', views.profil, name="accountprofil"),
    path('account/parametre', views.parametre, name="accountparametre"),
    path('account/suggestion', views.suggestion , name="accountsuggestion"),
    path('account/profil/competence', views.addcompetence, name="addcompetence"),
    path('account/profil/localisation', views.addlocalisation, name="addlocalisation"),
    path('account/profil/diplome', views.adddiplome, name="adddiplome"),
    path('account/profil/changepass', views.changepass, name="accountchangepass"),
    path('account/favoris', views.favoris, name="accountfavoris"),
    path('account/favoris/<int:job_id>/', views.addfavoris, name="addfavoris"),
    path('account/dashboard', views.dashboard, name="accountdashboard"),
    path('about/', views.about, name="about"),
    path('connexion/', views.connexion, name="connexion"),
    path('connexion/', views.connexion, name="deconnexion"),
    path('demandeur_emploi/', views.demandeur_emploi, name="demandeur_emploi"),
    path('employeur/', views.employeur, name="employeur"),
    path('inscription/', views.inscription, name="inscription"),
    path('liste_offre/<int:page>/', views.liste_offre2, name="liste_offre2"),
    path('liste_offre/', views.liste_offre, name="liste_offre"),
    path('detail/<int:job_id>/', views.detail, name="detail"),
    path('account/supprimer_competence', views.supprimer_competence, name="supprimer_competence"),
    path('categorie/<path:categorie>', views.categorie, name="categorie"),
    path('categorie/<int:page>/<path:categorie>/', views.categorie2, name="categorie2"),
]
if settings.DEBUG:   
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 