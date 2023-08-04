from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import CharField, EmailField, ModelChoiceField, ModelForm, Select, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from biryong.competition.models import Team

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password', "last_login", "is_superuser", "groups", "profile_photo_link", "active", "email",
                   "is_active", "is_staff", "username", "date_joined", "user_permissions", "academic_backgrounds", "careers", ]


class AdditionalInfoForm(ModelForm):
    support_team = ModelChoiceField(queryset=Team.objects.all(), widget=Select(attrs={'class': 'form-select'}))
    cheer_message = CharField(widget=Textarea(
        attrs={'class': 'form-control', 'placeholder': '응원 메시지를 입력해주세요.', 'rows': 5}))
    twitch_id = CharField(required=False, widget=TextInput(attrs={'class': 'form-control',
                          'placeholder': '트위치 아이디를 입력해주세요.'}))

    class Meta:
        model = User
        fields = ["support_team", "cheer_message", "twitch_id"]
