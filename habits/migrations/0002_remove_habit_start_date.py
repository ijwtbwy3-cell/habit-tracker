from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='start_date',
        ),
    ]
