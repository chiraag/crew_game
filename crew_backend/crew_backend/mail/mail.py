import base64
from email.mime.text import MIMEText
from typing import Dict

from googleapiclient.errors import HttpError
from jinja2 import Environment, PackageLoader, Template

from crew_game.backend.mail import gmail

JINJA_ENV = Environment(loader=PackageLoader("crew_game", "backend/mail/templates"))


def create_message(to_addr: str, subject: str, template: Template, data: dict):
    body = template.render(data)

    message = MIMEText(body)
    message["to"] = to_addr
    message["from"] = "admin@chiraagjuvekar.com"
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


# Add more providers (like SMTP) here eventually

EmailError = HttpError


def send_message(message: str) -> None:
    gmail.send_message(message)


def send(to_addr: str, subject: str, template_name: str, data: Dict):
    template = JINJA_ENV.get_template(template_name)
    message = create_message(to_addr, subject, template, data)
    send_message(message)
