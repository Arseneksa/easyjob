from .models import *
from django import forms
class CreateImageForm(forms.ModelForm):
	description = forms.CharField(widget = forms.Textarea(
		attrs = {
			'class':'form-control',
			'placeholder':'donner une description de limage',
		}
	))
	ville = forms.CharField(widget = forms.TextInput(
		attrs = {
			'class':'form-control',
			'placeholder':'nom de la ville',
		}
	))
	image_profil = forms.ImageField(widget = forms.ClearableFileInput(
			attrs = {
				'class':'btn btn-default',
			}
		))
	class Meta:
		model = CreateImage
		# fields = ('description',)
		# fields = '__all__'
		exclude = ('date',)

class CategorieImageForm(forms.ModelForm):
	"""docstring for CategorieImage"""
	class Meta:
		model = CategorieImage
		exclude = ('numeroCategorie',)
		

class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = '__all__'

class GroupeForm(forms.ModelForm):
	class Meta:
		model = Groupe
		fields = '__all__'
class EquipeForm(forms.ModelForm):
	class Meta:
		model = Equipe
		fields = '__all__'


