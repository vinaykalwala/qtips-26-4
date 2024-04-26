from django import forms
from .models import Variants

class VariantSelectionForm(forms.Form):
    size = forms.ChoiceField(choices=(), required=False)
    color = forms.ChoiceField(choices=(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].choices = self.get_size_choices()
        self.fields['color'].choices = self.get_color_choices()

    def get_size_choices(self):
        sizes = Variants.objects.values_list('size__name', flat=True).distinct()
        return [(size, size) for size in sizes]

    def get_color_choices(self):
        colors = Variants.objects.values_list('color__name', flat=True).distinct()
        return [(color, color) for color in colors]