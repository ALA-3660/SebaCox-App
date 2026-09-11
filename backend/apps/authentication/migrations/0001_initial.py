import django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion
import apps.authentication.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mobile_number', models.CharField(db_index=True, help_text='Primary authentication identifier in canonical format (+8801XXXXXXXXX).', max_length=20, unique=True, validators=[apps.authentication.validators.validate_bd_mobile_number])),
                ('email', models.EmailField(blank=True, help_text='Optional contact and notification email address.', max_length=254, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.')),
                ('is_verified', models.BooleanField(db_index=True, default=False, help_text="Designates whether the user's mobile number has been verified via OTP.")),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time the user account was created.')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mobile_number', models.CharField(db_index=True, max_length=20, validators=[apps.authentication.validators.validate_bd_mobile_number])),
                ('otp_hash', models.CharField(help_text='SHA-256 cryptographic hash of salt + raw OTP. Never store plaintext.', max_length=128)),
                ('salt', models.CharField(help_text='Random cryptographic salt for OTP hashing.', max_length=32)),
                ('purpose', models.CharField(choices=[('REGISTRATION', 'Registration'), ('LOGIN', 'Login'), ('PHONE_VERIFICATION', 'Phone Verification'), ('PASSWORD_RESET', 'Password Reset')], db_index=True, max_length=30)),
                ('expires_at', models.DateTimeField(db_index=True)),
                ('attempts', models.PositiveIntegerField(default=0, help_text='Number of incorrect verification attempts.')),
                ('max_attempts', models.PositiveIntegerField(default=5, help_text='Maximum allowed attempts before invalidation.')),
                ('is_consumed', models.BooleanField(db_index=True, default=False, help_text='Whether this OTP has already been verified and used.')),
                ('consumed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'OTP Verification',
                'verbose_name_plural': 'OTP Verifications',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuthAuditLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mobile_number', models.CharField(db_index=True, max_length=20)),
                ('event', models.CharField(choices=[('OTP_REQUESTED', 'OTP Requested'), ('OTP_VERIFIED', 'OTP Verified'), ('LOGIN_SUCCESS', 'Login Success'), ('LOGIN_FAILED', 'Login Failed'), ('LOGOUT', 'Logout'), ('TOKEN_REFRESH_SUCCESS', 'Token Refresh Success'), ('TOKEN_REFRESH_FAILED', 'Token Refresh Failed'), ('ACCOUNT_ACTIVATED', 'Account Activated')], db_index=True, max_length=40)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, default='', max_length=255)),
                ('details', models.JSONField(blank=True, default=dict, help_text='Non-sensitive event metadata. NEVER store secrets.')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='auth_audit_logs', to='authentication.user')),
            ],
            options={
                'verbose_name': 'Auth Audit Log',
                'verbose_name_plural': 'Auth Audit Logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['mobile_number'], name='auth_user_mobile__idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_active', 'is_verified'], name='auth_user_active__idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['created_at'], name='auth_user_created_idx'),
        ),
        migrations.AddIndex(
            model_name='otpverification',
            index=models.Index(fields=['mobile_number', 'purpose', 'is_consumed'], name='auth_otp_lookup_idx'),
        ),
        migrations.AddIndex(
            model_name='otpverification',
            index=models.Index(fields=['expires_at'], name='auth_otp_exp_idx'),
        ),
    ]
