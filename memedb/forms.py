from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms.widgets import ClearableFileInput
from django.urls import reverse_lazy


from .models import Meme


class MemeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Meme
        fields = [
            "content_",
            "tags",
        ]

    content_ = forms.ImageField(
        widget=ClearableFileInput(
            attrs={
                "hx-post": reverse_lazy("meme_create_suggested_tags"),
                "hx-target": "#suggested-tags",
                "hx-encoding": "multipart/form-data",
                "hx-swap": "outerHTML",
            }
        )
    )


class MemeCreateSuggestedTagsForm(forms.Form):
    content_ = forms.ImageField()


class MemeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Meme
        fields = [
            "tags",
        ]


class MemeDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(
            Submit("submit", "Confirm deletion", css_class="btn-danger")
        )
