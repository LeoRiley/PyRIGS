from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class BaseAsset(models.Model):
    class Meta:
        abstract = True

    parent = models.ForeignKey(to='self', related_name='asset_parent', blank=True, null=True, on_delete=models.SET_NULL)
    asset_id = models.CharField(max_length=10)
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
    length = models.DecimalField(decimal_places=1, max_digits=10, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('asset_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.asset_id) + ' - ' + self.description


# Automatically updates Asset.asset_id to Asset.pk if none is given by the user
@receiver(post_save, sender=Asset)
def update_asset_id(sender, instance, **kwargs):
    post_save.disconnect(update_asset_id, sender=sender)

    if not instance.asset_id:
        instance.asset_id = instance.pk
    instance.save()

    post_save.connect(update_asset_id, sender=sender)
