# Generated by Django 4.2.8 on 2024-11-21 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contestant', '0002_remove_contestant_birthday_alter_contestant_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('ip', models.GenericIPAddressField()),
                ('vote_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('score', models.JSONField(blank=True, default=list, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.SmallIntegerField(choices=[(0, 'male 0'), (1, 'girl 1'), (2, 'performance 2'), (3, 'boang 3')], default=0)),
                ('voted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contestant.contestant')),
            ],
        ),
    ]
