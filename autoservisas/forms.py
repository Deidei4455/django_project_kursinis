from django import forms

from .models import UzsakymasReview, Profile, User, Uzsakymas, PaslaugaUzsakymas


class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer')
        widgets = {
            'uzsakymas': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class DateInput(forms.DateInput):
    input_type = 'date'


class PaslaugaUzsakymasLine(forms.ModelForm):
    model = PaslaugaUzsakymas
    extra = 1
    fields = ('paslauga', 'paslaugu_kiekis')


class UserUzsakymasCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ('data', 'automobilis', 'uzsakovas', 'due_back', 'status')
        widgets = {
            'data': forms.HiddenInput(),
            'uzsakovas': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'due_back': DateInput()
        }
