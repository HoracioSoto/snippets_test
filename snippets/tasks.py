from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

@shared_task
def send_email_in_snippet_creation(snippet_name, snippet_description, user_mail):
    """
    Send an email notification to the user when a snippet is created.
    The email contains the snippet's name and description.
    """
    subject = 'Snippet "' + snippet_name + '" created successfully'
    body = (
        'The snippet "' + snippet_name + '" was created with the following description: \n'
        + snippet_description
    )

    # Only send the email if the user has registered an email address
    try:
        if user_mail:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user_mail],
                fail_silently=False,
            )
        print("Email sent successfully.")
    except Exception as e:
        # print and debug all the errors
        print("Error sending email:", e)
