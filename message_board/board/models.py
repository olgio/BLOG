from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    objects = None
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return f"{self.author} - {self.text}"

    class Meta:
        ordering = ['date_created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Comment(models.Model):
    objects = None
    comment = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def __str__(self):
        return f"{self.author} - {self.post} - {self.comment}"

    class Meta:
        ordering = ['date_created']
        verbose_name = 'Комментарий к сообщениям'
        verbose_name_plural = 'Комментарии к сообщениям'


# Cоздание профайла при создании User
class UserProfile(models.Model):
    objects = None
    user = models.OneToOneField(User, primary_key=True, verbose_name='Автор', related_name='profile',
                                on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя автора', max_length=20)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png',
                                blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def __str__(self):
    return self.user


class Meta:
    ordering = ["name"]
    verbose_name = "Имя автора"
    verbose_name_plural = "Имена авторов"



# def __str__(self) - Строка для представления объекта в административной панели и т.д.

# primary_key=True - предотвращения дублирования строк в модели в отношениях "один к одному"
# (предотвращение наличия у пользователя нескольких профилей)

# null=True - поле может не иметь значения, параметр относится непосредственно к базе данных.
# blank=True - поле может быть пустым в формах, относится к валидации данных на уровне Django, а не базы данных.
# verbose_name - удобочитаемое имя для поля
# related_name - для взаимодействия с базой данных
