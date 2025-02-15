from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


class Gamintojas(models.Model):
    gamintojas = models.CharField("Gamintojas", max_length=30)

    def __str__(self):
        return f"{self.gamintojas}"

    class Meta:
        verbose_name = 'Gamintojas'
        verbose_name_plural = 'Gamintojai'


class Modelis(models.Model):
    modelis = models.CharField("Modelis", max_length=20,
                               help_text="Įveskite automobilio modelį")
    gamintojas = models.ForeignKey(Gamintojas, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.modelis}"

    class Meta:
        verbose_name = 'Modelis'
        verbose_name_plural = 'Modeliai'


class Klientas(models.Model):
    f_name = models.CharField("Vardas", max_length=30)
    l_name = models.CharField("Pavardė", max_length=30)
    numeris = models.CharField("Numeris", max_length=30)

    def __str__(self):
        return f"{self.f_name} {self.l_name} {self.numeris}"

    class Meta:
        verbose_name = 'Klientas'
        verbose_name_plural = 'Klientai'


class Car(models.Model):
    autonr = models.CharField("Automobilio numeris", max_length=6)
    modelis = models.ForeignKey(Modelis, on_delete=models.SET_NULL, null=True)
    klientas = models.ForeignKey(Klientas, on_delete=models.SET_NULL, null=True)
    car_img = models.ImageField('Auto img', upload_to='cars', null=True, blank=True)

    aprasymas = HTMLField(null=True, blank=True)

    def __str__(self):
        return (f"{self.modelis.gamintojas.gamintojas} "
                f"{self.modelis.modelis} "
                f"{self.autonr} ")

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

    def display_klientas(self):
        return f"{self.klientas.f_name} {self.klientas.l_name} {self.klientas.numeris}"

    def display_car(self):
        return f"{self.modelis.gamintojas.gamintojas} {self.modelis.modelis} {self.autonr}"


class Paslaugos(models.Model):
    paslauga = models.CharField("Paslauga", max_length=50)
    aprasymas = models.CharField("Aprašymas", max_length=500,
                                 help_text="Aprašykite paslaugą")
    kaina = models.FloatField("Paslaugos kaina", max_length=30)

    def __str__(self):
        return f"{self.paslauga}, kaina - {self.kaina}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Uzsakymas(models.Model):
    data = models.DateField("Užsakymo data", null=True, blank=True, default=date.today())

    uzsakovas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    ORDER_STATUS = (
        ('a', 'Apdorojamas'),
        ('p', 'Priimtas'),
        ('v', 'Vykdomas'),
        ('i', 'Įvykdytas')
    )

    status = models.CharField('Statusas',
                              max_length=1,
                              choices=ORDER_STATUS,
                              default='a',
                              blank=True,
                              help_text='Užsakymo statusas')

    due_back = models.DateField("Grąžinimo data", null=True, blank=True)

    @property
    def is_late(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    @property
    def bendra_kaina(self):
        suma = 0
        paslaugos = PaslaugaUzsakymas.objects.filter(uzsakymas=self)
        for paslauga_uzsakymas in paslaugos:
            suma += paslauga_uzsakymas.paslaugu_kiekis * paslauga_uzsakymas.paslauga.kaina

        return suma

    automobilis = models.ForeignKey(Car, on_delete=models.CASCADE)

    def display_cars(self):
        return (f"{self.automobilis.modelis.gamintojas.gamintojas} "
                f"{self.automobilis.modelis.modelis} ")

    def __str__(self):
        return (f"status: {self.status}, "
                f"užsakymo data: {self.data}, "
                f"bendra kaina: {self.bendra_kaina}")

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'


class PaslaugaUzsakymas(models.Model):
    paslaugu_kiekis = models.IntegerField("Paslagų kiekis",
                                          help_text="Kiek kartų ši paslauga bus vykdoma")

    paslauga = models.ForeignKey(Paslaugos, on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE)

    @property
    def kaina(self):
        return self.paslaugu_kiekis * self.paslauga.kaina

    def __str__(self):
        return (f"Paslaugos kiekis: {self.paslaugu_kiekis}, "
                f"paslauga: {self.paslauga.paslauga}, "
                f"užsakymo statusas: {self.uzsakymas.status}")

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymų eilutės'


class UzsakymasReview(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Komentaras', max_length=2000)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE, blank=True)

    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date_created}, {self.reviewer}, {self.uzsakymas}, {self.content[:50]}"


class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', default='default_user.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)
