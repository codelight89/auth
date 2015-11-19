import hashlib
import random
import datetime

from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import logout, login
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from . import forms
from models import Account


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(function=view, login_url="/")


class RegisterUserView(FormView):
    form_class = forms.AccountCreationForm

    template_name = "registration/registration.html"

    def form_valid(self, form):
        user = form.save()
        email = user.email

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + email).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        user.activation_key = activation_key
        user.key_expires = key_expires
        user.save()
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours %s/confirm/%s" % (email.split("@")[0], settings.BASE_URL, activation_key)

        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
        return HttpResponseRedirect('/register_success')


class LoginFormView(FormView):
    form_class = forms.AccountAuthenticationForm
    template_name = "registration/login.html"
    success_url = "/home"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect("/", {})


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = "registration/base.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context["username"] = self.request.user.email.split("@")[0]
        return context


class RegisterSuccess(TemplateView):

    template_name = "registration/registration_success.html"


class RegisterConfirm(View):
    @staticmethod
    def get(request, activation_key):
        if request.user.is_authenticated():
            HttpResponseRedirect('/home')
        user = get_object_or_404(Account, activation_key=activation_key)

        if user.key_expires + datetime.timedelta(days=2) <= timezone.now():
            return render_to_response("registration/confirm_expired.html")

        user.is_active = True
        user.save()
        return HttpResponseRedirect('/home')

