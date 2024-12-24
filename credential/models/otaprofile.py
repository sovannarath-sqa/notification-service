from django.db import models

class OTAProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Optional: add a string representation for the model (useful for debugging)
    def __str__(self):
        return self.name
    
    # Meta options, for example, to specify the default ordering of records
    class Meta:
        ordering = ['-created_at']  # Ordering by created_at (newest first)
        app_label = 'credential'