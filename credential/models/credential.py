from django.db import models
from . import otaprofile
from . import propertyprofile

class Credential(models.Model):
    
    id = models.AutoField(primary_key=True)
    ota = models.ForeignKey(otaprofile.OTAProfile, on_delete=models.CASCADE)
    property = models.ForeignKey(propertyprofile.PropertyProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    channel_id = models.IntegerField()
    f_no = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Credential for {self.username} (Property ID: {self.property_id})"
    
    class Meta:
        # Optionally, set constraints or indexing for better performance
        db_table = 'credentials'
        indexes = [
            models.Index(fields=['property_id', 'ota_id', 'username']),
        ]
        app_label = 'credential'