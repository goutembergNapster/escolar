from django import forms
from .models import Escola

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola  # O modelo que o formulário representa
        fields = '__all__'

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remover a máscara do CNPJ caso tenha sido inserida
            cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        return cnpj