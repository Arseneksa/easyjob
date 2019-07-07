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
from EasyJob.views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
app_name = 'easyjob'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('base/', base, name="base"),
    path('', index, name="home"),
    path('default', default, name="default"),
    path('home/<int:job_id>/', home2, name="accounthome"),
    path('home/', home, name="accounthome"),
    path('account/profil', profil, name="accountprofil"),
    path('account/parametre', parametre, name="accountparametre"),
    path('account/suggestion', suggestion , name="accountsuggestion"),
    path('account/profil/competence', addcompetence, name="addcompetence"),
    path('account/profil/localisation', addlocalisation, name="addlocalisation"),
    path('account/profil/diplome', adddiplome, name="adddiplome"),
    path('account/profil/changepass', changepass, name="accountchangepass"),
    path('account/favoris', favoris, name="accountfavoris"),
    path('account/favoris/<int:job_id>/', addfavoris, name="addfavoris"),
    path('account/dashboard', dashboard, name="accountdashboard"),
    path('about/', about, name="about"),
    path('connexion/', connexion, name="connexion"),
    path('connexion/', connexion, name="deconnexion"),
    path('demandeur_emploi/', demandeur_emploi, name="demandeur_emploi"),
    path('employeur/', employeur, name="employeur"),
    path('inscription/', inscription, name="inscription"),
    path('liste_offre/<int:page>/', liste_offre2, name="liste_offre2"),
    path('liste_offre/', liste_offre, name="liste_offre"),
    path('detail/<int:job_id>/', detail, name="detail"),
    path('account/supprimer_competence', supprimer_competence, name="supprimer_competence"),
    path('categorie/<path:categorie>', categorie, name="categorie"),
    path('categorie/<int:page>/<path:categorie>/', categorie2, name="categorie2"),
]
if settings.DEBUG:   
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
