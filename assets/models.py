import re
from django.core.exceptions import ValidationError
from django.db import models, connection
from django.urls import reverse


class AssetCategory(models.Model):
    class Meta:
        verbose_name = 'Asset Category'
        verbose_name_plural = 'Asset Categories'

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class AssetStatus(models.Model):
    class Meta:
        verbose_name = 'Asset Status'
        verbose_name_plural = 'Asset Statuses'

    name = models.CharField(max_length=80)
    should_show = models.BooleanField(default=True, help_text="Should this be shown by default in the asset list.")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        permissions = (
            ('view_supplier', 'Can view a supplier'),
        )

    def get_absolute_url(self):
        return reverse('supplier_list')

    def __str__(self):
        return self.name


class Connector(models.Model):
    description = models.CharField(max_length=80)
    current_rating = models.DecimalField(decimal_places=2, max_digits=10, help_text='Amps')
    voltage_rating = models.IntegerField(help_text='Volts')
    num_pins = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.description


class Asset(models.Model):
    class Meta:
        ordering = ['asset_id']
        permissions = (
            ('asset_finance', 'Can see financial data for assets'),
            ('view_asset', 'Can view an asset')
        )

    parent = models.ForeignKey(to='self', related_name='asset_parent', blank=True, null=True, on_delete=models.SET_NULL)
    asset_id = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120)
    category = models.ForeignKey(to=AssetCategory, on_delete=models.CASCADE)
    status = models.ForeignKey(to=AssetStatus, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=150, blank=True)
    purchased_from = models.ForeignKey(to=Supplier, on_delete=models.CASCADE, blank=True, null=True)
    date_acquired = models.DateField()
    date_sold = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    salvage_value = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    comments = models.TextField(blank=True)
    next_sched_maint = models.DateField(blank=True, null=True)

    # Cable assets
    is_cable = models.BooleanField(default=False)
    plug = models.ForeignKey(Connector, on_delete=models.SET_NULL, related_name='plug', blank=True, null=True)
    socket = models.ForeignKey(Connector, on_delete=models.SET_NULL, related_name='socket', blank=True, null=True)
    length = models.DecimalField(decimal_places=1, max_digits=10, blank=True, null=True, help_text='m')
    csa = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, help_text='mm^2')
    circuits = models.IntegerField(blank=True, null=True)
    cores = models.IntegerField(blank=True, null=True)

    def get_available_asset_id():
        sql = """
        SELECT MIN(CAST(a.asset_id AS int))+1
        FROM assets_asset a
        LEFT OUTER JOIN assets_asset b ON
            (CAST(a.asset_id AS int) + 1 = CAST(b.asset_id AS int))
        WHERE b.asset_id IS NULL AND CAST(a.asset_id AS int) >= %s;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [9000])
            row = cursor.fetchone()
            if row[0] is None:
                return 9000
            else:
                return row[0]

    def get_absolute_url(self):
        return reverse('asset_detail', kwargs={'pk': self.asset_id})

    def __str__(self):
        out = str(self.asset_id) + ' - ' + self.description
        if self.is_cable:
            out += '{} - {}m - {}'.format(self.plug, self.length, self.socket)
        return out

    def clean(self):
        errdict = {}
        if self.date_sold and self.date_acquired > self.date_sold:
            errdict["date_sold"] = ["Cannot sell an item before it is acquired"]

        self.asset_id = self.asset_id.upper()
        if re.search("^[a-zA-Z0-9]+$", self.asset_id) is None:
                errdict["asset_id"] = ["An Asset ID can only consist of letters and numbers"]

        if self.purchase_price and self.purchase_price < 0:
            errdict["purchase_price"] = ["A price cannot be negative"]

        if self.salvage_value and self.salvage_value < 0:
            errdict["salvage_value"] = ["A price cannot be negative"]

        if self.is_cable:
            if not self.length or self.length <= 0:
                errdict["length"] = ["The length of a cable must be more than 0"]
            if not self.csa or self.csa <= 0:
                errdict["csa"] = ["The CSA of a cable must be more than 0"]
            if not self.circuits or self.circuits <= 0:
                errdict["circuits"] = ["There must be at least one circuit in a cable"]
            if not self.cores or self.cores <= 0:
                errdict["cores"] = ["There must be at least one core in a cable"]
            if self.socket is None:
                errdict["socket"] = ["A cable must have a socket"]
            if self.plug is None:
                errdict["plug"] = ["A cable must have a plug"]

        if errdict != {}:  # If there was an error when validation
            raise ValidationError(errdict)
