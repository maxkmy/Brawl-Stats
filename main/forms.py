from django import forms 

class PlayerForm(forms.Form):
	playerTag = forms.CharField(label='text-input', max_length=20,
				widget=forms.TextInput(attrs={'placeholder': 'Player Tag (e.g. 989C0QQ)'}))