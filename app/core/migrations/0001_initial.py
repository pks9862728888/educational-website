# Generated by Django 3.0.8 on 2020-07-26 18:29

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='Email')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('is_student', models.BooleanField(default=False, verbose_name='Is Student')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='Is Teacher')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('is_active', 'user_is_active'), ('is_staff', 'user_is_staff'), ('is_student', 'user_is_student'), ('is_teacher', 'user_is_teacher')),
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.ProhibitNullCharactersValidator], verbose_name='Institute Name')),
                ('country', django_countries.fields.CountryField(countries=core.models.OperationalCountries, default='IN', max_length=2, verbose_name='Country')),
                ('institute_category', models.CharField(choices=[('E', 'EDUCATION'), ('A', 'ART'), ('M', 'MUSIC'), ('D', 'DANCE')], max_length=1, verbose_name='Institute Category')),
                ('type', models.CharField(choices=[('SC', 'SCHOOL'), ('CO', 'COLLEGE'), ('CC', 'COACHING')], max_length=2, verbose_name='Institute Type')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('institute_slug', models.SlugField(blank=True, max_length=180, null=True, verbose_name='Institute Slug')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='InstituteDiscountCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rs', models.BigIntegerField(verbose_name='Discount in Rupees')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('expiry_date', models.DateTimeField(verbose_name='Expiry Date')),
                ('coupon_code', models.SlugField(blank=True, unique=True, verbose_name='Coupon Code')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='institute_discount_coupon', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=70, validators=[django.core.validators.ProhibitNullCharactersValidator], verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=70, validators=[django.core.validators.ProhibitNullCharactersValidator], verbose_name='Last Name')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, verbose_name='Gender')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone')),
                ('date_of_birth', models.DateField(blank=True, max_length=10, null=True, verbose_name='Date of Birth')),
                ('country', django_countries.fields.CountryField(countries=core.models.OperationalCountries, default='IN', max_length=2, verbose_name='Country')),
                ('primary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], default='EN', max_length=3, verbose_name='Primary language')),
                ('secondary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, null=True, verbose_name='Secondary language')),
                ('tertiary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, null=True, verbose_name='Tertiary language')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, core.models.Languages),
        ),
        migrations.CreateModel(
            name='SystemMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('message', models.TextField(max_length=60, verbose_name='Message')),
                ('seen', models.BooleanField(default=False, verbose_name='Seen')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=1024, null=True, upload_to=core.models.user_profile_picture_upload_file_path, validators=[django.core.validators.validate_image_file_extension], verbose_name='Image')),
                ('uploaded_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Uploaded on')),
                ('class_profile_picture', models.BooleanField(default=False, verbose_name='ClassProfilePicture')),
                ('public_profile_picture', models.BooleanField(default=False, verbose_name='PublicProfilePicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_pictures', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile Pictures',
            },
        ),
        migrations.CreateModel(
            name='InstituteSelectedLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BAS', 'BASIC'), ('BUS', 'BUSINESS'), ('ENT', 'ENTERPRISE')], max_length=3, verbose_name='Type')),
                ('billing', models.CharField(choices=[('M', 'MONTHLY'), ('A', 'ANNUALLY')], max_length=1, verbose_name='Billing')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount In Rs')),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Discount In Percentage')),
                ('net_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Net Amount in Rs')),
                ('storage', models.IntegerField(verbose_name='Storage in GB')),
                ('no_of_admin', models.PositiveIntegerField(verbose_name='No of admin')),
                ('no_of_staff', models.PositiveIntegerField(verbose_name='No of staff')),
                ('no_of_faculty', models.PositiveIntegerField(verbose_name='No of faculty')),
                ('no_of_student', models.PositiveIntegerField(verbose_name='No of students')),
                ('video_call_max_attendees', models.PositiveIntegerField(verbose_name='Video call max attendees')),
                ('classroom_limit', models.PositiveIntegerField(verbose_name='Classroom Limit')),
                ('department_limit', models.PositiveIntegerField(verbose_name='Department Limit')),
                ('subject_limit', models.PositiveIntegerField(verbose_name='Subject Limit')),
                ('scheduled_test', models.BooleanField(verbose_name='Scheduled Test')),
                ('LMS_exists', models.BooleanField(blank=True, verbose_name='LMS exists')),
                ('discussion_forum', models.CharField(choices=[('O', 'ONE_PER_SUBJECT'), ('S', 'ONE_PER_SUBJECT_OR_SECTION')], max_length=1, verbose_name='Discussion forum')),
                ('discount_coupon', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.InstituteDiscountCoupon')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_selected_license', to='core.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='InstituteProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motto', models.TextField(blank=True, max_length=256, verbose_name='Motto')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone')),
                ('website_url', models.URLField(blank=True, verbose_name='Website Url')),
                ('state', models.CharField(blank=True, choices=[('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CH', 'Chandigarh'), ('CT', 'Chhattishgarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('LD', 'Lakshadweep'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MR', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PD', 'Pondicherry'), ('PB', 'Punjab'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TG', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UK', 'Uttarakhand'), ('WB', 'West Bengal')], max_length=2, verbose_name='State')),
                ('pin', models.CharField(blank=True, max_length=10, verbose_name='Pin Code')),
                ('address', models.TextField(blank=True, max_length=50, verbose_name='Address')),
                ('recognition', models.CharField(blank=True, max_length=30, verbose_name='Recognition')),
                ('primary_language', models.CharField(choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], default='EN', max_length=3, verbose_name='Primary Language')),
                ('secondary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, verbose_name='Secondary Language')),
                ('tertiary_language', models.CharField(blank=True, choices=[('EN', 'English'), ('BN', 'Bengali'), ('HI', 'Hindi')], max_length=3, verbose_name='Tertiary Language')),
                ('institute', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institute_profile', to='core.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='InstituteLogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=1024, null=True, upload_to=core.models.institute_logo_upload_file_path, validators=[django.core.validators.validate_image_file_extension], verbose_name='Logo')),
                ('uploaded_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Uploaded on')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_logo', to='core.Institute')),
            ],
            options={
                'verbose_name_plural': 'Institute Logos',
            },
        ),
        migrations.CreateModel(
            name='InstituteLicenseOrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_receipt', models.CharField(blank=True, max_length=27, verbose_name='Order receipt')),
                ('order_id', models.CharField(blank=True, max_length=100, verbose_name='Order Id')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Amount in Rupees')),
                ('currency', models.CharField(default='INR', max_length=4, verbose_name='Currency')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Order Created On')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='institute_license_order', to='core.Institute')),
                ('selected_license', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.InstituteSelectedLicense')),
            ],
        ),
        migrations.CreateModel(
            name='InstituteBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=1024, null=True, upload_to=core.models.institute_banner_upload_file_path, validators=[django.core.validators.validate_image_file_extension], verbose_name='Banner')),
                ('uploaded_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Uploaded on')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_banner', to='core.Institute')),
            ],
            options={
                'verbose_name_plural': 'Institute Banners',
            },
        ),
        migrations.CreateModel(
            name='InstitutePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'ADMIN'), ('S', 'STAFF'), ('F', 'FACULTY')], max_length=1, verbose_name='Permission')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Request Date')),
                ('request_accepted_on', models.DateTimeField(blank=True, null=True, verbose_name='Request Accept Date')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='core.Institute')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
                ('inviter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('institute', 'invitee')},
            },
        ),
        migrations.CreateModel(
            name='InstituteLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BAS', 'BASIC'), ('BUS', 'BUSINESS'), ('ENT', 'ENTERPRISE')], max_length=3, verbose_name='Type')),
                ('billing', models.CharField(choices=[('M', 'MONTHLY'), ('A', 'ANNUALLY')], max_length=1, verbose_name='Billing')),
                ('amount', models.BigIntegerField(verbose_name='Amount In Rs')),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Discount In Percentage')),
                ('storage', models.IntegerField(verbose_name='Storage in Gb')),
                ('no_of_admin', models.PositiveIntegerField(default=1, verbose_name='No of admin')),
                ('no_of_staff', models.PositiveIntegerField(default=0, verbose_name='No of staff')),
                ('no_of_faculty', models.PositiveIntegerField(default=0, verbose_name='No of faculty')),
                ('no_of_student', models.PositiveIntegerField(default=99999, verbose_name='No of students')),
                ('video_call_max_attendees', models.PositiveIntegerField(verbose_name='Video call max attendees')),
                ('classroom_limit', models.PositiveIntegerField(default=99999, verbose_name='Classroom Limit')),
                ('department_limit', models.PositiveIntegerField(default=0, verbose_name='Department Limit')),
                ('subject_limit', models.PositiveIntegerField(default=99999, verbose_name='Subject Limit')),
                ('scheduled_test', models.BooleanField(default=True, verbose_name='Scheduled Test')),
                ('LMS_exists', models.BooleanField(default=True, verbose_name='LMS exists')),
                ('discussion_forum', models.CharField(choices=[('O', 'ONE_PER_SUBJECT'), ('S', 'ONE_PER_SUBJECT_OR_SECTION')], max_length=1, verbose_name='Discussion forum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_licenses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('type', 'billing')},
            },
        ),
        migrations.CreateModel(
            name='InstituteClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('class_slug', models.CharField(blank=True, max_length=60, null=True, verbose_name='Class slug')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_classes', to='core.Institute')),
            ],
            options={
                'unique_together': {('institute', 'name')},
            },
        ),
    ]
