import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional, Union, cast

from app import logger
from app.config import MAIL_HOST, MAIL_PASS, MAIL_PORT, MAIL_USER

from .template import render_template


def send_email_by_template(
    to: Union[str, List[str]], template_filename: str, **template_data
):
    send_email(
        to,
        template_data["subject"],
        render_template(template_filename, **template_data),
    )


def send_email(
    to: Union[str, List[str]],
    subject: str,
    body: str,  # <- jinja html render
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    sender: str = MAIL_USER,
):
    """sends email using a Jinja HTML template"""

    # convert TO into list if string
    if type(to) is str:
        to = to.split()

    to_l = cast(List[str], to)
    to_list = to_l + ([cc] if cc else []) + ([bcc] if bcc else [])

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["Subject"] = subject
    msg["To"] = ",".join(to)
    msg["Cc"] = cc
    msg["Bcc"] = bcc
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
        try:
            logger.info("sending email")
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(sender, to_list, msg.as_string())
        except Exception as e:
            logger.error("Error sending email")
            logger.exception(str(e))
        finally:
            server.quit()
