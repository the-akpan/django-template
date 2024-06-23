from ..env import env

USERS_SETTINGS = {
    {%- if cookiecutter.username_type == "email" -%}
    "SUPERUSER_EMAIL": env("DJANGO_SUPERUSER_EMAIL", default="root@localhost.site"),
    {%- else -%}
    "SUPERUSER_USERNAME": env("DJANGO_SUPERUSER_USERNAME", default="admin"),
    {%- endif -%}
    "SUPERUSER_PASSWORD": env("DJANGO_SUPERUSER_PASSWORD", default="admin"),
}
