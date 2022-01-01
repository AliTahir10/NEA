from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
class Createuser(UserCreationForm):
    email = forms.EmailField(required=True,max_length=50)
    password1 = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def save(self,commit=True):
        user = super(Createuser, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
                user.save()
        return user

#class CustomerForm(ModelForm): # creating a form which will allow a user to create an account
#   password = forms.CharField(max_length=100, widget=forms.PasswordInput)
#  password2 = forms.CharField(max_length=100) # added custom fields on top of the set fields
#   last_name = forms.CharField(max_length=100) 
#
#    class Meta: #inheriting from the standard user form
#       model = Customer
#       fields = ['first_name','last_name' ,'email','password','password2']

class Enquire(ModelForm):
    date = forms.DateField()
    Customisation = forms.CharField(max_length=1000)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = Request
        fields = ['date','name','Customisation','paymethod','picture']

class Update(ModelForm):
    date = forms.DateField()
    Customisation = forms.CharField(max_length=1000)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Request
        fields = ['user','name','date','Customisation','paymethod','picture','price','status']

class blockday(ModelForm):
    date = forms.DateInput()

    class Meta:
        model = Block
        fields = ['date']

class Createproduct(ModelForm):

    class Meta:
        model = Product
        fields = ['name','category','minprice','Maxprice','picture','description']

class tags(ModelForm):

    class Meta:
        model = Producttag
        fields = ['tag','product']
