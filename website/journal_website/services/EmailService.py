from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


class EmailService:
    def send_email_message(self, sender, receiver, subject, email_template_name, code=None):
        content = {
            "email": receiver.email,
            'domain': '127.0.0.1:8000',
			'site_name': 'Website',
            "user": receiver,
			'protocol': 'http',
        }
        if code is not None:
            content["code"] = code
        else:
            content["uid"] = urlsafe_base64_encode(force_bytes(receiver.pk))
            content["token"] = default_token_generator.make_token(receiver)

        message = render_to_string(email_template_name, content)
        try:
            send_mail(subject, message, sender , [receiver.email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')