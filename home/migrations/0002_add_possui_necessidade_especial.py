from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='possui_necessidade_especial',
            field=models.BooleanField(default=False),
        ),
    ]
