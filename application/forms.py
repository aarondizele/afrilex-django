from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Expert


class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        # fields = '__all__'
        fields = ['firstname', 'lastname', 'slug', 'about']

    def clean_slug(self, *args, **kwargs):
        instance = self.instance
        slug = self.cleaned_data.get("slug")
        qs = Expert.objects.filter(slug__iexact=slug)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) ## id=instance.id
        if qs.exists():
            raise forms.ValidationError("This slug has already been used. Please try again")
        return slug


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Veuillez enter votre nom!", label="Nom")
    last_name = forms.CharField(max_length=30, required=True, help_text="Veuillez enter votre prénom!", label="Prénom")
    email = forms.EmailField(max_length=254, help_text="Veuillez entrer votre adresse email", label="Adresse email")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]