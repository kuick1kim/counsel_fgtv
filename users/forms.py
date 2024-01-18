from django import forms
from django.core.exceptions import ValidationError

from users.models import User




class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자명 (3자리 이상)"},
        ),
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 (4자리 이상)"},
        ),
    )

    
class UserProfileForm(forms.Form):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    profile_image = forms.ImageField(required=False)


    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"입력한 사용자명({username})은 이미 사용중입니다")
        return username

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            self.add_error("password2", "비밀번호와 비밀번호 확인란의 값이 다릅니다")

    def save(self):
        username = self.cleaned_data["username"]
        password1 = self.cleaned_data["password1"]

        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        phone_number = self.cleaned_data["phone_number"]
        profile_image = self.cleaned_data["profile_image"]
       
        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            profile_image=profile_image,
        )
        return user
