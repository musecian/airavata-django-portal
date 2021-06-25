import uuid

from django.conf import settings
from django.db import models

from . import forms
from django.core.exceptions import ValidationError

VERIFY_EMAIL_TEMPLATE = 1
NEW_USER_EMAIL_TEMPLATE = 2
PASSWORD_RESET_EMAIL_TEMPLATE = 3
USER_ADDED_TO_GROUP_TEMPLATE = 4
VERIFY_EMAIL_CHANGE_TEMPLATE = 5


class EmailVerification(models.Model):
    username = models.CharField(max_length=64)
    verification_code = models.CharField(
        max_length=36, unique=True, default=uuid.uuid4)
    created_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    next = models.CharField(max_length=255, blank=True)


class EmailTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = (
        (VERIFY_EMAIL_TEMPLATE, 'Verify Email Template'),
        (NEW_USER_EMAIL_TEMPLATE, 'New User Email Template'),
        (PASSWORD_RESET_EMAIL_TEMPLATE, 'Password Reset Email Template'),
        (USER_ADDED_TO_GROUP_TEMPLATE, 'User Added to Group Template'),
        (VERIFY_EMAIL_CHANGE_TEMPLATE, 'Verify Email Change Template'),
    )
    template_type = models.IntegerField(
        primary_key=True, choices=TEMPLATE_TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        for choice in self.TEMPLATE_TYPE_CHOICES:
            if self.template_type == choice[0]:
                return choice[1]
        return "Unknown"


class PasswordResetRequest(models.Model):
    username = models.CharField(max_length=64)
    reset_code = models.CharField(
        max_length=36, unique=True, default=uuid.uuid4)
    created_date = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="user_profile")
    # TODO: maybe this can be derived from whether there exists an Airavata
    # User Profile for the user's username
    username_locked = models.BooleanField(default=False)

    @property
    def is_complete(self):
        return (self.is_username_valid and
                self.is_first_name_valid and
                self.is_last_name_valid and
                self.is_email_valid)

    @property
    def is_username_valid(self):
        # use forms.USERNAME_VALIDATOR with an exception when the username is
        # equal to the email
        try:
            forms.USERNAME_VALIDATOR(self.user.username)
            validates = True
        except ValidationError:
            validates = False
        return (validates or (self.is_email_valid and self.user.email == self.user.username))

    @property
    def is_first_name_valid(self):
        return self.is_non_empty(self.user.first_name)

    @property
    def is_last_name_valid(self):
        return self.is_non_empty(self.user.last_name)

    @property
    def is_email_valid(self):
        # Only checking for non-empty only; assumption is that email is verified
        # before it is set or updated
        return self.is_non_empty(self.user.email)

    def is_non_empty(self, value: str):
        return value is not None and value.strip() != ""


class UserInfo(models.Model):
    claim = models.CharField(max_length=64)
    value = models.CharField(max_length=255)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_profile', 'claim']

    def __str__(self):
        return f"{self.claim}={self.value}"


class IDPUserInfo(models.Model):
    idp_alias = models.CharField(max_length=64)
    claim = models.CharField(max_length=64)
    value = models.CharField(max_length=255)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="idp_userinfo")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_profile', 'claim', 'idp_alias']

    def __str__(self):
        return f"{self.idp_alias}: {self.claim}={self.value}"


class PendingEmailChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_address = models.EmailField()
    verification_code = models.CharField(
        max_length=36, unique=True, default=uuid.uuid4)
    created_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
