from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location', 'address']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and Shop.objects.filter(name=name).exists():
            raise forms.ValidationError('A shop with this name already exists.')
        return name

    def clean_location(self):
        location = self.cleaned_data['location']
        # validation
        if location.x < -180 or location.x > 180:
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        if location.y < -90 or location.y > 90:
            raise forms.ValidationError("Latitude must be between -90 and 90.")

        return location



class UpdateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location', 'address']


