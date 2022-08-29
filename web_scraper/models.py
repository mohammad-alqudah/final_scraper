# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.CASCADE)
    permission = models.ForeignKey('AuthPermission', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    group = models.ForeignKey(AuthGroup, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MainappAddOns(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_add_ons'


class MainappAnnouncementCenter(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    brand_branch = models.ForeignKey('MainappBrandBranch', models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_announcement_center'


class MainappBrand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    partner_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=50)
    image = models.CharField(max_length=100, blank=True, null=True)
    talabat_commission = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    careem_commission = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    cs_mena_subscription = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    ask_paper_subscription = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_brand'


class MainappBrandBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField()
    careem_id = models.IntegerField()
    careem_name_status_tab = models.CharField(max_length=100, blank=True, null=True)
    csmena_name = models.CharField(max_length=50)
    askpaper_name = models.CharField(max_length=50)
    multiplayer_forecast = models.DecimalField(max_digits=5, decimal_places=3)
    fp_branch = models.ForeignKey('MainappFpBranch', models.CASCADE, db_column='Fp_branch_id', blank=True, null=True)  # Field name made lowercase.
    brand = models.ForeignKey(MainappBrand, models.CASCADE)
    talabat_id = models.IntegerField(blank=True, null=True)
    talabat_name = models.CharField(max_length=100, blank=True, null=True)
    makane_name= models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_brand_branch'


class MainappChannel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40)
    monthly_fees = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_channel'


class MainappDays(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'mainapp_days'


class MainappFp(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_fp'


class MainappFpBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    area = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    bilding_no = models.CharField(max_length=20)
    active = models.BooleanField()
    sales_tax = models.DecimalField(max_digits=5, decimal_places=3)
    revenue_percentage = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    other_expenses = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fp = models.ForeignKey(MainappFp, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_fp_branch'


class MainappIncidentReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    case_date_time = models.DateTimeField(blank=True, null=True)
    message = models.CharField(max_length=100, blank=True, null=True)
    pdf_link = models.CharField(max_length=200, blank=True, null=True)
    brand_branch = models.ForeignKey(MainappBrandBranch, models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey(MainappChannel, models.CASCADE, blank=True, null=True)
    liability = models.ForeignKey('MainappLiability', models.CASCADE)
    type_rating = models.ForeignKey('MainappTypeRating', models.CASCADE)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_incident_report'


class MainappItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_item'


class MainappKitchefyUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    postion = models.CharField(max_length=40)
    role = models.CharField(max_length=50)
    user = models.OneToOneField(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_kitchefy_user'


class MainappKnowleddgeCenterSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'mainapp_knowleddge_center_section'


class MainappKnowledgeCenter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    video_link = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    fp = models.ForeignKey(MainappFp, models.CASCADE)
    knowledge_center_section = models.ForeignKey(MainappKnowleddgeCenterSection, models.CASCADE)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_knowledge_center'


class MainappLiability(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_liability'


class MainappOffers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField()
    soft_delete = models.BooleanField()
    brand_branch = models.ForeignKey(MainappBrandBranch, models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey(MainappChannel, models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_offers'


class MainappOpeningHours(models.Model):
    id = models.BigAutoField(primary_key=True)
    start = models.TimeField()
    end = models.TimeField()
    brand_branch = models.ForeignKey(MainappBrandBranch, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_opening_hours'


class MainappOpeningHoursDay(models.Model):
    id = models.BigAutoField(primary_key=True)
    opening_hours = models.ForeignKey(MainappOpeningHours, models.CASCADE)
    days = models.ForeignKey(MainappDays, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_opening_hours_day'
        unique_together = (('opening_hours', 'days'),)


class MainappOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    total = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    delivery_zone = models.CharField(max_length=50, blank=True, null=True)
    details = models.CharField(max_length=500, blank=True, null=True)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    customer_mobile_number = models.CharField(max_length=50, blank=True, null=True)
    payment_fees = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    delivary_fee = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    brand_branch = models.ForeignKey(MainappBrandBranch, models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey(MainappChannel, models.CASCADE, blank=True, null=True)
    gross_basket = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    payment_handling_charges = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    pg_fees = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    promo_code = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
     
    class Meta:
        managed = False
        db_table = 'mainapp_order'


class MainappOrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(max_length=5)
    price = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    item = models.ForeignKey(MainappItem, models.CASCADE)
    order = models.ForeignKey(MainappOrder, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mainapp_order_item'


class MainappOrderItemAddOns(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    add_ons = models.ForeignKey(MainappAddOns, models.CASCADE, db_column='Add_ons_id', blank=True, null=True)  # Field name made lowercase.
    order_item = models.ForeignKey(MainappOrderItem, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_order_item_add_ons'


class MainappStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    brand_branch = models.ForeignKey(MainappBrandBranch, models.CASCADE, db_column='Brand_branch_id')  # Field name made lowercase.
    channel = models.ForeignKey(MainappChannel, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mainapp_status'


class MainappTypeRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'mainapp_type_rating'
