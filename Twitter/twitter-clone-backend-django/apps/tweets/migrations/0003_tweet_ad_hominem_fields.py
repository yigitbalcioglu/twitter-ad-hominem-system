from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tweet",
            name="ad_hominem_checked_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="tweet",
            name="ad_hominem_score",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tweet",
            name="is_ad_hominem",
            field=models.BooleanField(blank=True, db_index=True, null=True),
        ),
    ]
