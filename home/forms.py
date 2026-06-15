from cProfile import label

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    subject = forms.CharField(label='Subject', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your subject'}))
    message = forms.CharField(label='Message Body', max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message body'}))


class CommentForm(forms.Form):
    content = forms.CharField(label='Comment', max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment'}))