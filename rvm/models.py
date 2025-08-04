from django.db import models
from django.contrib.auth.models import User

class Deposit(models.Model):
    MATERIAL_CHOICES = [
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    weight = models.FloatField()
    material = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    machine_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.material} - {self.weight}kg"
