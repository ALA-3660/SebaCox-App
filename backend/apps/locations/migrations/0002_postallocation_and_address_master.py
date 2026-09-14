import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='aliases',
            field=models.JSONField(blank=True, default=list, help_text='বিকল্প নাম বা উপনামসমূহ (e.g. Kolatoli, Kalatali, কলাতলী)'),
        ),
        migrations.AddField(
            model_name='locality',
            name='source',
            field=models.CharField(blank=True, default='Field Survey / BBS / Local Verification', help_text='তথ্যসূত্র বা উৎস', max_length=150),
        ),
        migrations.AddField(
            model_name='locality',
            name='verification_status',
            field=models.CharField(choices=[('UNVERIFIED', 'যাচাই করা হয়নি (Unverified)'), ('FIELD_VERIFIED', 'মাঠ পর্যায়ে যাচাইকৃত (Field Verified)'), ('OFFICIALLY_CONFIRMED', 'প্রশাসনিকভাবে অনুমোদিত (Officially Confirmed)')], db_index=True, default='FIELD_VERIFIED', help_text='যাচাইকরণের অবস্থা', max_length=30),
        ),
        migrations.CreateModel(
            name='PostalLocation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, help_text='বাংলায় ভৌগোলিক ইউনিটের নাম (e.g. চট্টগ্রাম, কক্সবাজার সদর)', max_length=150)),
                ('name_en', models.CharField(db_index=True, help_text="Geographic unit name in English (e.g. Chattogram, Cox's Bazar Sadar)", max_length=150)),
                ('code', models.CharField(blank=True, db_index=True, help_text='Administrative code or BBS geocode', max_length=20, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='সক্রিয় অবস্থা (Active status for filtering)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post_office_name_bn', models.CharField(db_index=True, help_text='ডাকঘরের নাম বাংলায় (e.g. কক্সবাজার প্রধান ডাকঘর, ঝিলংঝা সাব-পোস্ট অফিস)', max_length=150)),
                ('post_office_name_en', models.CharField(db_index=True, help_text="Post office name in English (e.g. Cox's Bazar Head Post Office, Jhilongjha Sub Post Office)", max_length=150)),
                ('post_code', models.CharField(db_index=True, help_text='৪-সংখ্যার পোস্ট কোড (e.g. 4700, 4701, 4702)', max_length=10)),
                ('aliases', models.JSONField(blank=True, default=list, help_text='বিকল্প নাম বা ডাকঘরের পরিচিত উপনামসমূহ')),
                ('source', models.CharField(default='Bangladesh Post Master / BBS', help_text='তথ্যসূত্র বা উৎস', max_length=100)),
                ('verification_status', models.CharField(choices=[('UNVERIFIED', 'যাচাই করা হয়নি (Unverified)'), ('FIELD_VERIFIED', 'মাঠ পর্যায়ে যাচাইকৃত (Field Verified)'), ('OFFICIALLY_CONFIRMED', 'প্রশাসনিকভাবে অনুমোদিত (Officially Confirmed)')], db_index=True, default='OFFICIALLY_CONFIRMED', max_length=30)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postal_locations', to='locations.district')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postal_locations', to='locations.municipality')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postal_locations', to='locations.union')),
                ('upazila', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postal_locations', to='locations.upazila')),
            ],
            options={
                'verbose_name': 'ডাকঘর অবস্থান (Postal Location)',
                'verbose_name_plural': 'ডাকঘর অবস্থানসমূহ (Postal Locations)',
                'ordering': ['post_code', 'name_en'],
            },
        ),
        migrations.AddField(
            model_name='userlocation',
            name='detailed_address',
            field=models.CharField(blank=True, default='', help_text='বিস্তারিত ঠিকানা (ঐচ্ছিক)', max_length=255),
        ),
        migrations.AddField(
            model_name='userlocation',
            name='postal_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.postallocation'),
        ),
    ]
