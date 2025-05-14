from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments import highlight

def get_highlighted_snippet(snippet):
    """
    Returns the highlighted version of a code snippet.
    """
    lexer = get_lexer_by_name(snippet.language.slug)
    formatter = HtmlFormatter()
    return highlight(snippet.snippet, lexer, formatter)
