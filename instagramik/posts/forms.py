from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['description', 'image']
        labels = {
            'description': 'Описание поста',
            'image': 'Ваше фото',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напишите здесь что-нибудь'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

