import os

from fastapi import HTTPException, status
from jinja2 import Template

from app.config import TEMPLATES_FOLDER, templateEnv


def render_template(TEMPLATE_FILENAME: str, **kwargs) -> str:
    file_path = os.path.join(TEMPLATES_FOLDER, TEMPLATE_FILENAME)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"template {TEMPLATE_FILENAME} no existe",
        )
    template: Template = templateEnv.get_template(TEMPLATE_FILENAME)
    return template.render(**kwargs)
