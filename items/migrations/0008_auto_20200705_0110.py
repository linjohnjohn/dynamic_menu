# Generated by Django 3.0.7 on 2020-07-05 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('internal_name', models.CharField(max_length=200)),
                ('markup', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ingredients', models.ManyToManyField(blank=True, to='items.Ingredient')),
                ('item', models.ManyToManyField(blank=True, to='items.Item')),
            ],
        ),
        migrations.RemoveField(
            model_name='itemvariant',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='itemvariant',
            name='item',
        ),
        migrations.DeleteModel(
            name='CategoryVariant',
        ),
        migrations.DeleteModel(
            name='ItemVariant',
        ),
    ]
