from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreatedForm(forms.ModelForm):

    class Meta:
        models = Image
        fields = ('title','url', 'description')
        widget = {
            'url' : forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extentions = ['jpg','jpeg']
        extentions = url.rsplit('.',1)[1].lower()
        if extentions not in valid_extentions:
            raise forms.ValidationError('The given URL does ot match valid image extention')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreatedForm, self).save(commit=False)
        image_url =self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.',1)[1].lower())

        #download image from the given url
        response = request.urlopen(image_url)
        image.image.save(image_name,
                        ContentFile(response.read()),
                        save=False)
        
        if commit:
            image.save()
        return image