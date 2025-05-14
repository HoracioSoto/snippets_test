from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.urls import reverse

from .forms import SnippetForm
from .models import Snippet
from .utils import get_highlighted_snippet

class SnippetAdd(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new snippet.
    """
    extra_context = {"action": "Cargar"}
    form_class = SnippetForm
    model = Snippet
    template_name = "snippets/snippet_add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("snippet", kwargs={"id": self.object.id})


class SnippetEdit(LoginRequiredMixin, UpdateView):
    """
    View to handle the editing of an existing snippet.
    """
    extra_context = {"action": "Editar"}
    form_class = SnippetForm
    model = Snippet
    template_name = "snippets/snippet_add.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("snippet", kwargs={"id": self.object.id}) 


class SnippetDelete(LoginRequiredMixin, DeleteView):
    """
    View to handle the deletion of a snippet.
    """
    def get(self, request, *args, **kwargs):
        snippet_id = kwargs["id"]
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except Snippet.DoesNotExist:
            return render(request, "snippets/404.html", status=404)
        if snippet.user != request.user:
            return render(request, "snippets/404.html", status=404)
        snippet.delete()
        return redirect("user_snippets", username=request.user.username)


class SnippetDetails(View):
    """
    View to display the details of a snippet.
    """
    form_class = SnippetForm
    model = Snippet

    def get(self, request, **kwargs):
        """
        Renders the snippet details page.
        """
        snippet_id = kwargs["id"]
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except Snippet.DoesNotExist:
            return render(request, "snippets/404.html", status=404)
        # Add conditions for private snippets
        if not snippet.public and snippet.user != request.user:
            return render(request, "snippets/404.html", status=404)
        # Highlight the snippet using Pygments
        snippet.snippet = get_highlighted_snippet(snippet)
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )


class UserSnippets(View):
    """
    View to display all snippets of a specific user.
    """
    form_class = SnippetForm
    model = Snippet

    def get(self, request, *args, **kwargs):
        username = kwargs["username"]
        if request.user.is_authenticated and request.user.username == username:
            snippets = Snippet.objects.filter(user__username=username)
        else:
            snippets = Snippet.objects.filter(user__username=username, public=True)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )


class SnippetsByLanguage(View):
    """
    View to display snippets filtered by language.
    """
    def get(self, request, *args, **kwargs):
        """
        Renders all the public snippets filtered by an specific language.
        """
        language = self.kwargs["language"]
        return render(
            request,
            "index.html",
            {"snippets": Snippet.objects.filter(language__slug=language, public=True)}
        )


class Login(View):
    """
    View to handle user login.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is redirected to the index if it's already authenticated.
        """
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        Renders the login form if the user is not authenticated.
        """
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        """
        Handles the login form submission.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('index')
        return render(request, 'login.html', {'form': form})


class Logout(View):
    """
    View to handle user logout.
    """
    def get(self, request):
        """
        Logs out the user and redirects it to the index.
        """
        logout(request)
        return redirect('index')

class Index(View):
    """
    View to render the index page with all public snippets.
    """
    def get(self, request, *args, **kwargs):
        """
        Renders the index page with all public snippets.
        """
        return render(
            request,
            "index.html",
            {"snippets": Snippet.objects.filter(public=True)}
        )
