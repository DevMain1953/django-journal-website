# Generated by Django 4.2 on 2023-04-08 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_website', '0002_userpersonaldata_alter_article_user_delete_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpersonaldata',
            options={'verbose_name_plural': 'user_personal_data'},
        ),
    ]