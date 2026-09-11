import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import apps.locations.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=10, unique=True)),
                ('iso3', models.CharField(blank=True, max_length=3, null=True)),
                ('dial_code', models.CharField(blank=True, default='+880', max_length=10)),
                ('currency_code', models.CharField(blank=True, default='BDT', max_length=5)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'দেশ (Country)',
                'verbose_name_plural': 'দেশসমূহ (Countries)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='locations.country')),
            ],
            options={
                'verbose_name': 'বিভাগ (Division)',
                'verbose_name_plural': 'বিভাগসমূহ (Divisions)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='locations.division')),
            ],
            options={
                'verbose_name': 'জেলা (District)',
                'verbose_name_plural': 'জেলাসমূহ (Districts)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='Upazila',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upazilas', to='locations.district')),
            ],
            options={
                'verbose_name': 'উপজেলা (Upazila)',
                'verbose_name_plural': 'উপজেলাসমূহ (Upazilas)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='CityCorporation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_corporations', to='locations.district')),
            ],
            options={
                'verbose_name': 'সিটি কর্পোরেশন (City Corporation)',
                'verbose_name_plural': 'সিটি কর্পোরেশনসমূহ (City Corporations)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', to='locations.district')),
                ('upazila', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='municipalities', to='locations.upazila')),
            ],
            options={
                'verbose_name': 'পৌরসভা (Municipality)',
                'verbose_name_plural': 'পৌরসভাসমূহ (Municipalities)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='Union',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('upazila', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unions', to='locations.upazila')),
            ],
            options={
                'verbose_name': 'ইউনিয়ন (Union)',
                'verbose_name_plural': 'ইউনিয়নসমূহ (Unions)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ward_number', models.PositiveSmallIntegerField()),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city_corporation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='locations.citycorporation')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='locations.municipality')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='locations.union')),
            ],
            options={
                'verbose_name': 'ওয়ার্ড (Ward)',
                'verbose_name_plural': 'ওয়ার্ডসমূহ (Wards)',
                'ordering': ['ward_number'],
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(db_index=True, max_length=150)),
                ('name_en', models.CharField(db_index=True, max_length=150)),
                ('code', models.CharField(db_index=True, max_length=20, validators=[apps.locations.validators.validate_location_code])),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localities', to='locations.municipality')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localities', to='locations.union')),
                ('upazila', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localities', to='locations.upazila')),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localities', to='locations.ward')),
            ],
            options={
                'verbose_name': 'এলাকা / পাড়া (Locality)',
                'verbose_name_plural': 'এলাকাসমূহ (Localities)',
                'ordering': ['name_en'],
            },
        ),
        migrations.CreateModel(
            name='GeoLocation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, validators=[apps.locations.validators.validate_latitude])),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, validators=[apps.locations.validators.validate_longitude])),
                ('srid', models.IntegerField(default=4326)),
                ('address_text', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.country')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.district')),
                ('locality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.locality')),
                ('upazila', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.upazila')),
            ],
            options={
                'verbose_name': 'ভৌগোলিক অবস্থান (GeoLocation)',
                'verbose_name_plural': 'ভৌগোলিক অবস্থানসমূহ (GeoLocations)',
            },
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('location_type', models.CharField(choices=[('SELECTED', 'নির্বাচিত সেবা এলাকা (Selected Service Area)'), ('CURRENT', 'বর্তমান জিপিএস অবস্থান (Current GPS Location)'), ('PREFERRED', 'পছন্দনীয় এলাকা (Preferred Location)'), ('HOME', 'বাসা (Home)'), ('WORK', 'কর্মস্থল (Work)'), ('OTHER', 'অন্যান্য (Other Saved Place)')], db_index=True, default='SELECTED', max_length=20)),
                ('label', models.CharField(blank=True, default='', max_length=100)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.country')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.district')),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.division')),
                ('geo_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_associations', to='locations.geolocation')),
                ('locality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.locality')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.municipality')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.union')),
                ('upazila', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.upazila')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_locations', to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.ward')),
            ],
            options={
                'verbose_name': 'ব্যবহারকারীর অবস্থান (User Location)',
                'verbose_name_plural': 'ব্যবহারকারীর অবস্থানসমূহ (User Locations)',
            },
        ),
        migrations.CreateModel(
            name='ServiceArea',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name_bn', models.CharField(max_length=150)),
                ('name_en', models.CharField(max_length=150)),
                ('area_type', models.CharField(choices=[('ADMINISTRATIVE', 'প্রশাসনিক সীমানা (Administrative Boundaries)'), ('RADIUS', 'নির্দিষ্ট ব্যাসার্ধ (Radial Distance)')], default='ADMINISTRATIVE', max_length=20)),
                ('radius_km', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[apps.locations.validators.validate_radius])),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('center_geo_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.geolocation')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.district')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.union')),
                ('upazila', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.upazila')),
            ],
            options={
                'verbose_name': 'সেবা এলাকা (Service Area)',
                'verbose_name_plural': 'সেবা এলাকাসমূহ (Service Areas)',
            },
        ),
        migrations.AddConstraint(
            model_name='division',
            constraint=models.UniqueConstraint(fields=('country', 'code'), name='unique_division_country_code'),
        ),
        migrations.AddConstraint(
            model_name='division',
            constraint=models.UniqueConstraint(fields=('country', 'name_en'), name='unique_division_country_name_en'),
        ),
        migrations.AddConstraint(
            model_name='district',
            constraint=models.UniqueConstraint(fields=('division', 'code'), name='unique_district_division_code'),
        ),
        migrations.AddConstraint(
            model_name='district',
            constraint=models.UniqueConstraint(fields=('division', 'name_en'), name='unique_district_division_name_en'),
        ),
        migrations.AddConstraint(
            model_name='upazila',
            constraint=models.UniqueConstraint(fields=('district', 'code'), name='unique_upazila_district_code'),
        ),
        migrations.AddConstraint(
            model_name='upazila',
            constraint=models.UniqueConstraint(fields=('district', 'name_en'), name='unique_upazila_district_name_en'),
        ),
        migrations.AddConstraint(
            model_name='citycorporation',
            constraint=models.UniqueConstraint(fields=('district', 'code'), name='unique_city_corporation_district_code'),
        ),
        migrations.AddConstraint(
            model_name='municipality',
            constraint=models.UniqueConstraint(fields=('district', 'code'), name='unique_municipality_district_code'),
        ),
        migrations.AddConstraint(
            model_name='union',
            constraint=models.UniqueConstraint(fields=('upazila', 'code'), name='unique_union_upazila_code'),
        ),
        migrations.AddIndex(
            model_name='geolocation',
            index=models.Index(fields=['latitude', 'longitude'], name='idx_geo_lat_lng'),
        ),
        migrations.AddIndex(
            model_name='userlocation',
            index=models.Index(fields=['user', 'location_type'], name='idx_user_loc_type'),
        ),
    ]
