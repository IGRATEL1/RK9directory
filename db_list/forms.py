from django import forms

from .models import Materials_stats

class PostForm(forms.ModelForm):
    class Meta:
        model = Materials_stats
        fields = ('title','strength_limit','modulus_of_elasticity','yield_strength','elongation','poisson_ratio','ansys_file','graph_file')