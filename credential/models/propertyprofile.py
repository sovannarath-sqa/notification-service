from django.db import models


class PropertyProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, null=True, blank=True)
    suitebook_id = models.IntegerField()
    aos_slug = models.CharField(max_length=255, unique=True)
    aos_organization_name = models.CharField(max_length=255)
    aos_organization_slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property Profile"
        verbose_name_plural = "Property Profiles"
        db_table = "property_profile"  # Optional, to specify a custom table name
        ordering = ["-created_at"]  # Optional, to order by creation time by default
        app_label = "credential"
