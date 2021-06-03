from django import forms

class loginForm(forms.Form):
    Username = forms.CharField(max_length=30, widget=forms.TextInput(attrs= {'placeholder':'Username'}))
    Password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs= {'placeholder':'Password'}))
