from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model
from django.utils.translation import gettext_lazy as _

from biryong.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("LDN", {"fields":     ("kakao_id",
                                "profile_image_url",
                                "thumbnail_image_url",
                                "support_team",
                                "cheer_message",
                                "twitch_id",
                                "info_complete",
                                "competition1_winner_expect",
                                "competition2_winner_expect",
                                "competition3_winner_expect",
                                "competition1_POG",
                                "competition2_POG",
                                "competition3_POG",
                                "MVP",
                                "MEP")}),
        (_("Personal info"), {"fields": ("nickname",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "email", "nickname", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
