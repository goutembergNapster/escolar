from django.db import migrations

def convert_outro_to_responsavel(apps, schema_editor):
    Responsavel = apps.get_model("home", "Responsavel")
    Responsavel.objects.filter(tipo="outro").update(tipo="responsavel")

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_responsavel_tipo'),
    ]

    operations = [
        migrations.RunPython(convert_outro_to_responsavel),
    ]
