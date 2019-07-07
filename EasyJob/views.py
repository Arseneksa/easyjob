#-*- coding: utf-8 -*

from django.contrib.auth.decorators import login_required, permission_required 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.db.models import Q
from django.template import RequestContext
from .models import *
#import requests
#from geopy.geocoders import Nominatim
from django.core.paginator import Paginator, EmptyPage


def default(request):
    return render(request, 'default.html', {})

def base(request):
    return render(request,'base.html')


#Page Acceuil
def index(request):
    
#    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
#    my_ip = ip_request.json()['ip']
#    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
#    geo_request = requests.get(geo_request_url)
#    geo_data = geo_request.json()
#    
    error = False
    if request.method == "POST":
        form1 = SearchForm(request.POST)
        if form1.is_valid():
            motcle = form1.cleaned_data["motcle"]
            localite= form1.cleaned_data["localite"]
            
    else:
        form1 = SearchForm()
        
    request.session['ville'] = 'yaounde'
    #return HttpResponse( )
#    
    offres_proche = Job.objects.filter(localisation = request.session['ville']).order_by('-pubdate')[0:8]
    offres_recente = Job.objects.all().order_by('-pubdate')[0:8]
    
    return render(request,'index.html', locals(), {'offres_proche':offres_proche, 'offres_recente':offres_recente})
    
#Page a propos
def about(request):
    return render(request,'about.html')


#page déconnexion

#Page connexion
def connexion(request):
    
    logout(request)
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                request.session['user_id'] = request.user.id
                login(request, user)  # nous connectons l'utilisateur
                return redirect('accounthome')
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
        
    response = render(request,'registration/login.html', locals())
    response.delete_cookie('Yaounde')
    response.delete_cookie('Douala')
    response.delete_cookie('Maroua')
    response.delete_cookie('Bamenda')
    response.delete_cookie('Bafoussam')
    response.delete_cookie('Buea')
    response.delete_cookie('Ebolowa')
    response.delete_cookie('Bertoua')
    response.delete_cookie('Garoua')
    response.delete_cookie('Ngaoundere')
    
    return response




#Page Demande emploi
def demandeur_emploi(request):
    if request.method == "POST":
            form = SearchForm(request.POST)
            if form.is_valid():
                motcle= form.cleaned_data["motcle"]
                liste_motcle = motcle.split(" ")

                localite= form.cleaned_data["localite"]
                
                request.session['motcle'] = motcle
                request.session['localite'] = localite
    else:
            form = SearchForm()
    
    
    #offres = Job.objects.filter(town__icontains = 'douala')
    #return render(request,'liste_offres.html', {'motcle':motcle, 'localite':localite, 'offres':offres, 'pages':pages, 'nb_offres':nb_offres, 'categorie':categorie})
    return render(request,'demandeur_emploi.html', locals(),{'form':form})





#Page employeur
def employeur(request):
    return render(request,'employeur.html')




#Page inscription

def inscription(request):
    # if this is a POST request we need to process the form data
    template = 'inscription.html'
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form, 
                    'error_message': 'l\'email  exist déja.'
                })
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form, 
                    'error_message': 'Le nom exist déja.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form, 
                    'error_message': 'Mot de passe non identique.'
                })
            else:
                 # Ne sauvegarde pas directement l'article dans la base de données
                mot_de_passe = form.cleaned_data['password']
                utilisateur = form.save(commit=False) 
                utilisateur.localisation = 'Yaoundé'
                utilisateur.Telephone = (int)(form.cleaned_data['telephone'])
                utilisateur.set_password(mot_de_passe)
                
                utilisateur.save();                
                
                # Login the user
                #login(request, user)
                
                # redirect to accounts page:
                return redirect('connexion')

    # No post data availabe, let's just show the page.
    else:
        form = InscriptionForm()

    return render(request, template, {'form': form})





#vue liste des offres
def liste_offre(request):
        
    if request.method == "POST":
            form = SearchForm(request.POST)
            if form.is_valid():
                motcle= form.cleaned_data["motcle"]
                liste_motcle = motcle.split(" ")

                localite= form.cleaned_data["localite"]
                
                request.session['motcle'] = motcle
                request.session['localite'] = localite
    else:
            form = SearchForm()
            return redirect('home')
    
    offres = Job.objects.filter(
    
        Q(localisation__icontains = localite),
        Q(category__icontains = motcle),
        Q(description__icontains = motcle)|
        Q(title__icontains = motcle)
    
    ).order_by('-pubdate')
    
    p = Paginator(offres, 7)
    
    categorie= {}
    job= Job.objects.all().order_by('category')
    for elt in job:
        categorie[elt.category] = elt.category
        
        
    pages = {}
    i=0
    
    while(i < p.num_pages):
        i=i+1
        pages[i] = p.num_pages
    
    nb_offres = p.count

    offres = p.page(1)
    #return HttpResponse(localite)
    #offres = Job.objects.filter(town__icontains = 'douala')
    return render(request,'liste_offres.html', {'motcle':motcle, 'localite':localite, 'offres':offres, 'pages':pages, 'nb_offres':nb_offres, 'categorie':categorie})
    
    #vue liste des offres
def liste_offre2(request, page):
    
    motcle = request.session['motcle'] 
    localite = request.session['localite'] 
    
    offres = Job.objects.filter(
    
        Q(localisation__icontains = localite),
       (
            Q(category__icontains = motcle)|
            Q(description__icontains = motcle)
            
        )|
        Q(title__icontains = motcle)
    
    
    ).order_by('-pubdate')
        
    categorie= {}
    job= Job.objects.all().order_by('category')
    for elt in job:
        categorie[elt.category] = elt.category
        
        
    p = Paginator(offres, 7)
    
    pages = {}
    i=0
    
    while(i < p.num_pages):
        i=i+1
        pages[i] = p.num_pages
        
    nb_offres = p.count
    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger        
        offres = p.page(page)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
         offres = p.page(p.num_pages)
    #return HttpResponse(categorie) 
    #offres = Job.objects.filter(town__icontains = 'douala')
    return render(request,'liste_offres.html', {'motcle':motcle, 'localite':localite, 'offres':offres, 'pages':pages, 'nb_offres':nb_offres, 'categorie':categorie})


def categorie(request, categorie):
    template= 'categorie.html'
    offres = Job.objects.filter(category = categorie ).order_by('category')
        
    categories= {}
    job= Job.objects.all().order_by('category')
    for elt in job:
        categories[elt.category] = elt.category
        
        
    p = Paginator(offres, 7)
    
    pages = {}
    i=0
    
    while(i < p.num_pages):
        i=i+1
        pages[i] = p.num_pages
        
    nb_offres = p.count
    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger        
        offres = p.page(1)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
         offres = p.page(p.num_pages)
    #return HttpResponse(categorie) 
    #offres = Job.objects.filter(town__icontains = 'douala')
    return render(request,template, {'offres':offres, 'pages':pages, 'nb_offres':nb_offres, 'categorie':categorie, 'categories':categories})

def categorie2(request, page, categorie):
    
    template= 'categorie.html'
    offres = Job.objects.filter(category = categorie ).order_by('category')
        
    categories= {}
    job= Job.objects.all().order_by('category')
    for elt in job:
        categories[elt.category] = elt.category
        
        
    p = Paginator(offres, 7)
    
    pages = {}
    i=0
    
    while(i < p.num_pages):
        i=i+1
        pages[i] = p.num_pages
        
    nb_offres = p.count
    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger        
        offres = p.page(page)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
         offres = p.page(p.num_pages)
    #return HttpResponse(categorie) 
    #offres = Job.objects.filter(town__icontains = 'douala')
    return render(request,template, {'offres':offres, 'pages':pages, 'nb_offres':nb_offres, 'categorie':categorie, 'categories':categories})

#Page detail sur les offres
def detail (request, job_id):
    
    offre = Job.objects.get(id=job_id)
    
    return render(request,'detail.html', {'offre':offre})


#Page acceuil compte
@login_required(login_url='connexion/')
def home(request):
    
    user_id= request.user.id
    
    user =  Utilisateur.objects.get(id= user_id)
    
    offres = Job.objects.filter(
    
        Q(localisation__icontains = user.localisation),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    ).order_by('-pubdate')
    
    p = Paginator(offres, 10)

    pages = {}
    i=0
    while(i < p.num_pages):
            i=i+1
            pages[i] = p.num_pages
    
    #return HttpResponse(user.specialite)
    return render(request,'account/home.html', {'offres':offres, 'pages':pages})

@login_required(login_url='connexion/')
def home2(request, page):
    
    user_id= request.user.id
    
    user =  Utilisateur.objects.get(id= user_id)
    
    
    p = Paginator(offres, 10)

    pages = {}
    i=0
    while(i < p.num_pages):
            i=i+1
            pages[i] = p.num_pages
        
    try:
        # La définition de nos URL autorise comme argument « page » uniquement 
        # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger        
        offres = p.page(page)
    except EmptyPage:
        # Nous vérifions toutefois que nous ne dépassons pas la limite de page
        # Par convention, nous renvoyons la dernière page dans ce cas
        offres = p.page(p.num_pages)
    
    #return HttpResponse(user.specialite)
    return render(request,'account/home.html', {'offres':offres, 'pages':pages})



#Page  profil compte
@login_required(login_url='connexion/')
def profil(request):
    
    utilisateur = Utilisateur.objects.get(id=request.user.id)
    
    form = AddCompetenceForm(request.POST)
    form1 = AddLocalisationForm(request.POST)
    form2 = AddDiplomeForm(request.POST)
    return render(request,'account/profile.html', {'form':form, 'form1':form1, 'form2':form2,  'utilisateur':utilisateur})

#page favoris
@login_required(login_url='connexion/')
def favoris(request):
    #offres =  Job.objects.filter(town__icontains='douala')[0:4] 
    user_id= request.user.id
    favoris = Favoris.objects.filter(user__id = user_id)
    offres = {}
    #offres =  Job.objects.filter()
    i=0
    for fav in favoris:
        #liste = { }
        
        #return HttpResponse(favoris[i].job_id)
        offres[i] = Job.objects.get(id =fav.job_id)
        #listes = Job.objects.filter(job_id = cle)
        i=i+1
        
    #for job in offres :
        
    #return HttpResponse(offres[2].id)    
    return render(request,'account/favoris.html', {'offres':offres})
    



def addfavoris(request, job_id): 
    user_id= request.user.id
    
    user = Utilisateur.objects.get(id=user_id)
    
    job =  Job.objects.get(id= job_id)
    favoris = Favoris( user= user , job= job )
    
    if not Favoris.objects.filter(user=user , job=job).exists():
        favoris.save()
        
    
    #offres = Job.objects.filter(town__icontains = 'douala')
    return redirect('accounthome')




#page dashboard
@login_required(login_url='connexion/')
def dashboard(request):
    
    user_id= request.user.id
    
    user =  Utilisateur.objects.get(id= user_id)
    
    yaounde = Job.objects.filter(
    
        Q(localisation__icontains = 'Yaoundé'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    douala = Job.objects.filter(
    
        Q(localisation__icontains = 'douala'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    maroua  = Job.objects.filter(
    
        Q(localisation__icontains = 'maroua'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    bafoussam  = Job.objects.filter(
    
        Q(localisation__icontains = 'bafoussam'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    bamenda  = Job.objects.filter(
    
        Q(localisation__icontains = 'bamenda'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    buea  = Job.objects.filter(
    
        Q(localisation__icontains = 'Buéa'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    ebolowa  = Job.objects.filter(
    
        Q(localisation__icontains = 'ebolowa'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    bertoua  = Job.objects.filter(
    
        Q(localisation__icontains = 'bertoua'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    garoua  = Job.objects.filter(
    
        Q(localisation__icontains = 'garoua'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )
    ngaoundere  = Job.objects.filter(
    
        Q(localisation__icontains = 'Ngaoundéré'),
        (
            
            Q(title__icontains = user.specialite)|
            Q(category__icontains = user.specialite)        
            
        ),
        Q(description__icontains = user.specialite),
        Q(description__icontains = user.competence)
    
    
    )

    
    taille  = Job.objects.all().count()
    
    nb_yaounde =(float)(yaounde.count())
    nb_douala =(float)(douala.count())
    nb_maroua =(float)(maroua.count())
    nb_bamenda =(float)(bamenda.count())
    nb_bafoussam =(float)(bafoussam.count())
    nb_buea =(float)(buea.count())
    nb_ebolowa =(float)(ebolowa.count())
    nb_bertoua =(float)(bertoua.count())
    nb_garoua =(float)(garoua.count())
    nb_ngaoundere =(float)(ngaoundere.count())
    
    
    response =render(request,'account/dashboard.html', {'user':user})
    response.set_cookie('Yaounde', nb_yaounde)
    response.set_cookie('Douala', nb_douala)
    response.set_cookie('Maroua', nb_maroua)
    response.set_cookie('Bamenda', nb_bamenda)
    response.set_cookie('Bafoussam', nb_bafoussam)
    response.set_cookie('Buea', nb_buea)
    response.set_cookie('Ebolowa', nb_ebolowa)
    response.set_cookie('Bertoua', nb_bertoua)
    response.set_cookie('Garoua', nb_garoua)
    response.set_cookie('Ngaoundere', nb_ngaoundere)
    
    return response


#page changer mot de passe
@login_required(login_url='connexion/')
def changepass(request):
    form = ChangePassForm(request.POST)
    user = User.objects.get(id=request.user.id)
    if form.is_valid():
            oldpassword = form.cleaned_data["oldpassword"]
            newpassword= form.cleaned_data["newpassword"]
            #if user.check_password(oldpassword)
                #user.set_password( newpassword )
               # user.save() 
            #else:
                #return render(request,'account/profile.html', locals(), {'error_message': 'Mot de passe non identique.'}) 
    else:
        form = ChangePassForm()
        return redirect('accountprofil')
    return render(request,'account/profile.html', {'form': form})

def addcompetence(request):
    form = AddCompetenceForm(request.POST)
    
    utilisateur = Utilisateur.objects.get(id=request.user.id)
    
    if form.is_valid():
            competence = form.cleaned_data["Competence"]
            utilisateur.competence = competence;
            utilisateur.save()
            return redirect('accountprofil')
    else:
        form = AddCompetenceForm(request.POST)
        return redirect('accountprofil')
    return render(request,'account/profile.html', {'form': form})


def addlocalisation(request):
    form1 = AddLocalisationForm(request.POST)
    
    utilisateur = Utilisateur.objects.get(id=request.user.id)
    
    if form1.is_valid():
            localisation = form1.cleaned_data["localisation"]
            utilisateur.localisation = localisation;
            utilisateur.save()
            return redirect('accountprofil')
    else:
        form1 = AddLocalisationForm(request.POST)
        return redirect('accountprofil')
    form1 = AddLocalisationForm(request.POST)
    return render(request,'account/profile.html', {'form1':form1})


def adddiplome(request):
    form2 = AddDiplomeForm(request.POST)
    
    utilisateur = Utilisateur.objects.get(id=request.user.id)
    
    if form2.is_valid():
            diplome = form2.cleaned_data["diplome"]
            utilisateur.diplome = diplome;
            utilisateur.save()
            return redirect('accountprofil')
    else:
        form2 = AddDiplomeForm(request.POST)
        return redirect('accountprofil')
    form2 = AddLocalisationForm(request.POST)
    return render(request,'account/profile.html', {'form2':form2})




def parametre(request):
   
    return render(request,'account/parametre.html')



def suggestion(request):
    
    return render(request,'account/suggestion.html')

def supprimer_competence(request):
    utilisateur = Utilisateur.objects.get(id=request.user.id)
    
    utilisateur.competence = ' '
    utilisateur.save()
    return redirect('accountprofil')