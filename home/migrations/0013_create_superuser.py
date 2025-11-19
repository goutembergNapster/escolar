from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="bergadmin",
            email="goutemberg@icloud.com",
            password=make_password("Gps34587895@&*"),
            is_staff=True,
            is_superuser=True,
        )

def remove_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),  # ajuste para sua primeira migration
    ]

    operations = [
        migrations.RunPython(create_admin, remove_admin),
    ]
