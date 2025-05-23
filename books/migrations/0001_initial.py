# Generated by Django 5.1.5 on 2025-04-21 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
        ('categories', '0001_initial'),
        ('publisher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='book_pdfs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.publisher')),
            ],
        ),
    ]
