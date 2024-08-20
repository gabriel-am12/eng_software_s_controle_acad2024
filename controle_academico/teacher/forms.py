from django import forms
from core.models import Frequencia, Nota

class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ['data', 'presente']

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['avaliacao', 'nota']
 