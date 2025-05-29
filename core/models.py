from django.db import models

# Create your models here.
# Модель организации
class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return self.inn

# Модель платежа
class Payment(models.Model):
    operation_id = models.UUIDField(unique=True)
    amount = models.BigIntegerField()
    payer = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='payments')
    document_number = models.CharField(max_length=64)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation_id}"