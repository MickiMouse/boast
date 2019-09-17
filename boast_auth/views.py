from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import \
    (LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView

from .models import BoastUser
from .forms import RegisterUserForm, EditProfileForm
from .utilities import signer


class BoastLoginView(LoginView):
    template_name = 'boasting_auth/login.html'


class BoastLogoutView(LogoutView):
    next_page = 'boast_auth:login'


class BoastRegisterView(CreateView):
    model = BoastUser
    template_name = 'boasting_auth/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('boast_auth:register_done')


class BoastRegisterDoneView(TemplateView):
    template_name = 'boasting_auth/register_done.html'


def activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'boasting_auth/bad_signature.html')
    user = get_object_or_404(BoastUser, username=username)
    if user.is_activated:
        template = 'boasting_auth/is_activated.html'
    else:
        template = 'boasting_auth/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'posts': user.posts.all(),
    }
    return render(request, 'boasting_auth/profile.html', context)


class BoastPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'reset_password/reset.html'
    subject_template_name = 'reset_password/subject.txt'
    email_template_name = 'reset_password/email.html'
    success_url = reverse_lazy('boast_auth:profile')
    success_message = 'Request sent, follow the link that will be in the letter to reset the password'


class BoastPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'reset_password/reset_confirm.html'
    post_reset_login = True
    success_url = reverse_lazy('boast_auth:profile')
    success_message = 'Password has been changed successful'


class BoastEditProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = BoastUser
    form_class = EditProfileForm
    template_name = 'boasting_auth/edit_profile.html'
    success_message = 'Successful'
    success_url = reverse_lazy('boast_auth:profile')
