from django.shortcuts import redirect

class LoginRequiredMixin:
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/register")
        return super().dispatch(request, *args, **kwargs)
