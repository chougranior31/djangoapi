from django.db import models
from cryptography.fernet import Fernet









class Medecin(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DemandeSoin(models.Model):
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Demande {self.id}: {self.description[:50]}..."








class Appointment(models.Model):
    name = models.CharField(max_length=122, blank=True, null=True)
    time = models.CharField(max_length=122, blank=True, null=True)
    encryption_key = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Générer une nouvelle clé de chiffrement si elle n'existe pas déjà
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key().decode()

        # Chiffrer les champs sensibles avant d'enregistrer l'instance
        cipher_suite = Fernet(self.encryption_key.encode())
        if self.name:
            self.name = cipher_suite.encrypt(self.name.encode()).decode()
        if self.time:
            self.time = cipher_suite.encrypt(self.time.encode()).decode()

        super().save(*args, **kwargs)

    def decrypt_fields(self):
        # Déchiffrer les champs sensibles
        cipher_suite = Fernet(self.encryption_key.encode())
        if self.name:
            self.name = cipher_suite.decrypt(self.name.encode()).decode()
        if self.time:
            self.time = cipher_suite.decrypt(self.time.encode()).decode()

    def __str__(self):
        return self.name
