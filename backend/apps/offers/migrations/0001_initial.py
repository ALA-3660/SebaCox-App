import django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('demands', '0001_initial'),
        ('providers', '0001_initial'),
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('version', models.PositiveIntegerField(db_index=True, default=1, help_text='চেইনে প্রস্তাবের সংস্করণ নম্বর (১, ২, ৩...)')),
                ('offer_type', models.CharField(choices=[('INITIAL', 'প্রাথমিক প্রস্তাব (Initial Offer)'), ('COUNTER', 'পাল্টা প্রস্তাব (Counter Offer)')], db_index=True, default='INITIAL', max_length=20)),
                ('status', models.CharField(choices=[('DRAFT', 'খসড়া'), ('PENDING', 'অপেক্ষমাণ'), ('ACCEPTED', 'গ্রহণ করা হয়েছে'), ('REJECTED', 'প্রত্যাখ্যাত'), ('CANCELLED', 'বাতিল'), ('EXPIRED', 'মেয়াদ শেষ'), ('SUPERSEDED', 'নতুন প্রস্তাবে প্রতিস্থাপিত')], db_index=True, default='PENDING', max_length=20)),
                ('title_bn', models.CharField(help_text='প্রস্তাবের শিরোনাম বাংলায়', max_length=255)),
                ('description_bn', models.TextField(blank=True, default='', help_text='প্রস্তাবের বিস্তারিত বিবরণ বাংলায়')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, help_text='কাজের বা সেবার পরিমাণ', max_digits=12, null=True)),
                ('unit', models.CharField(blank=True, default='', help_text='পরিমাপের একক', max_length=50)),
                ('price', models.DecimalField(decimal_places=2, help_text='মূল কাজের মূল্য (BDT)', max_digits=12)),
                ('currency', models.CharField(default='BDT', help_text='মুদ্রা কোড', max_length=10)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='পরিবহন বা ডেলিভারি ফি', max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='সার্ভিস বা অতিরিক্ত চার্জ', max_digits=12)),
                ('total_amount', models.DecimalField(decimal_places=2, help_text='সর্বমোট মূল্য (সার্ভার-সাইড নির্ধারিত)', max_digits=12)),
                ('terms_bn', models.TextField(blank=True, default='', help_text='প্রস্তাবের শর্তাবলী বাংলায়')),
                ('estimated_delivery_duration', models.CharField(blank=True, default='', help_text='আনুমানিক সময়কাল', max_length=100)),
                ('proposed_at', models.DateTimeField(default=django.utils.timezone.now, help_text='প্রস্তাব প্রেরণের সময়')),
                ('expires_at', models.DateTimeField(db_index=True, help_text='প্রস্তাবের মেয়াদ শেষ হওয়ার সময়')),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason_bn', models.TextField(blank=True, default='')),
                ('cancellation_reason_bn', models.TextField(blank=True, default='')),
                ('snapshot', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('demand', models.ForeignKey(help_text='সংশ্লিষ্ট প্রয়োজন (Demand)', on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='demands.demand')),
                ('match_candidate', models.ForeignKey(blank=True, help_text='উৎস ম্যাচিং ক্যান্ডিডেট রেফারেন্স', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='matching.matchcandidate')),
                ('parent_offer', models.ForeignKey(blank=True, help_text='পূর্ববর্তী প্রস্তাব', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='counter_offers', to='offers.offer')),
                ('proposer', models.ForeignKey(help_text='এই নির্দিষ্ট প্রস্তাব/পাল্টা-প্রস্তাব জমাদানকারী ব্যবহারকারী', on_delete=django.db.models.deletion.CASCADE, related_name='proposed_offers', to='authentication.user')),
                ('provider', models.ForeignKey(help_text='প্রস্তাবদাতা বা সংশ্লিষ্ট সেবাদাতা (Provider)', on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='providers.provider')),
                ('requester', models.ForeignKey(help_text='প্রয়োজন পোস্টকারী ব্যবহারকারী', on_delete=django.db.models.deletion.CASCADE, related_name='received_offers', to='authentication.user')),
                ('root_offer', models.ForeignKey(blank=True, help_text='চেইনের আদি প্রস্তাব', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chain_offers', to='offers.offer')),
            ],
            options={
                'verbose_name': 'প্রস্তাব (Offer)',
                'verbose_name_plural': 'প্রস্তাবসমূহ (Offers)',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OfferAuditLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('CREATED', 'প্রস্তাব তৈরি'), ('COUNTERED', 'পাল্টা প্রস্তাব প্রেরণ'), ('ACCEPTED', 'প্রস্তাব গৃহীত'), ('REJECTED', 'প্রস্তাব প্রত্যাখ্যাত'), ('CANCELLED', 'প্রস্তাব বাতিলকৃত'), ('EXPIRED', 'মেয়াদ উত্তীর্ণ'), ('SUPERSEDED', 'প্রতিস্থাপিত')], db_index=True, max_length=30)),
                ('previous_status', models.CharField(blank=True, default='', max_length=30)),
                ('new_status', models.CharField(blank=True, default='', max_length=30)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_audit_logs', to='authentication.user')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='offers.offer')),
            ],
            options={
                'verbose_name': 'অফার অডিট রেকর্ড (Offer Audit Log)',
                'verbose_name_plural': 'অফার অডিট রেকর্ডসমূহ (Offer Audit Logs)',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='offer',
            index=models.Index(fields=['demand', 'status'], name='offers_offe_demand__9652a2_idx'),
        ),
        migrations.AddIndex(
            model_name='offer',
            index=models.Index(fields=['provider', 'status'], name='offers_offe_provide_b6c5a1_idx'),
        ),
        migrations.AddIndex(
            model_name='offer',
            index=models.Index(fields=['requester', 'status'], name='offers_offe_request_b0ffcf_idx'),
        ),
        migrations.AddIndex(
            model_name='offer',
            index=models.Index(fields=['status', 'expires_at'], name='offers_offe_status__97cae9_idx'),
        ),
        migrations.AddIndex(
            model_name='offer',
            index=models.Index(fields=['root_offer', 'version'], name='offers_offe_root_of_0b4dc7_idx'),
        ),
        migrations.AddConstraint(
            model_name='offer',
            constraint=models.UniqueConstraint(fields=('demand', 'provider', 'version'), name='unique_demand_provider_version_offer'),
        ),
    ]
