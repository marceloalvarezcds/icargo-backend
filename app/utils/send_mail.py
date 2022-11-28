import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from typing import List, Optional

from app import logger
from app.config import (
    MAIL_ACTIVE,
    MAIL_HOST,
    MAIL_PASS,
    MAIL_PORT,
    MAIL_SSL,
    MAIL_TLS,
    MAIL_USER,
)

from .template import render_template


def send_email_with_template_by_thread(
    template_filename: str = "",
    to: str = "",
    subject: str = "",
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    sender: str = MAIL_USER,
    **template_data,
):
    if MAIL_ACTIVE:
        body = render_template(template_filename, **template_data)
        thread = Thread(
            target=send_email_in_thread,
            args=(to, subject, body, cc, bcc, sender),
        )
        thread.start()


def send_email_in_thread(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    sender: str = MAIL_USER,
):
    send_email(
        to.split(","),
        subject,
        body,
        cc,
        bcc,
        sender,
    )


def send_email(
    to_list: List[str],
    subject: str,
    body: str,  # <- jinja html render
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    sender: str = MAIL_USER,
):
    if MAIL_ACTIVE:
        all_to_list = to_list + ([cc] if cc else []) + ([bcc] if bcc else [])
        to = ",".join(all_to_list)
        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["Subject"] = subject
        msg["To"] = to
        msg["Cc"] = cc
        msg["Bcc"] = bcc
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            try:
                logger.info(f"sending email to {to}")
                context = ssl.create_default_context() if MAIL_SSL else None
                if MAIL_TLS:
                    server.starttls(context=context)
                server.login(MAIL_USER, MAIL_PASS)
                server.sendmail(sender, to_list, msg.as_string())
                logger.info("email sent successfully")
            except Exception as e:
                logger.error("Error sending email")
                logger.exception(str(e))
            finally:
                server.quit()
