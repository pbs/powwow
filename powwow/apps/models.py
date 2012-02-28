from django.db import models

SETTING_NAME = (
    ('conf_space', 'Confluence Space Key'),
    ('conf_page', 'Confluence Page'),
    ('jira_project', 'JIRA Project Code Name'),
    ('github_project', 'GitHub Project'),
)

class AppSettings(models.Model):
    name = models.CharField(max_length=50,
            primary_key=True,
            choices=SETTING_NAME)
    content = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "settings"
