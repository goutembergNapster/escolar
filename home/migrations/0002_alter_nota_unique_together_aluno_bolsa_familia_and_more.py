from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL("SELECT 1;", reverse_sql=migrations.RunSQL.noop),
    ]