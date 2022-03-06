from django import forms
from .models import Voter, County, Constituency, Ward


class VoterForm(forms.ModelForm):
    class Meta(object):
        model = Voter
        fields = '__all__'


class CountyForm(forms.ModelForm):
    class Meta(object):
        model = County
        fields = '__all__'
