from django import forms
from .models import Crop_info, Btn_display

class add_crop_details(forms.ModelForm):
    class Meta:
        model = Crop_info
        fields = ('farmer',
                  'crop_name',
                  'crop_species',
                  # 'geolocation_lat',
                  # 'geolocation_lon',
                  'crop_age',
                  'crop_height',)

class Btn_display(forms.ModelForm):
    class Meta:
        model = Btn_display
        fields = ()
# def typ2:
#     class meta:
#         model
#         fields x

# class block(forms.ModelForm):
#     crop_details = OneToOne
