from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout


class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        # TODO: Implement logic to get snippet by ID
        # snippet = Snippet.objects.get(id=snippet_id)
        # Add conditions for private snippets
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )  # Placeholder


class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        # TODO: Fetch user snippets based on username and public/private logic
        # snippets = Snippet.objects.filter(...)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        # TODO: Fetch snippets based on language
        return render(request, "index.html", {"snippets": []})  # Placeholder

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
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        return render(request, "index.html", {"snippets": []})  # Placeholder
