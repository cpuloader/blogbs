#coding: utf-8
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import blogbootstrap.settings as settings

class UserExtraFields(models.Model):
    baseuser = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255, verbose_name=_(u'Пара слов о себе'), 
                   default=u'Я новый юзер.', blank=True)
    picture = models.ImageField(default='profile_pics/default_profile.jpg',
                      upload_to='profile_pics', verbose_name=_(u'Фото'), blank=True)
    
    def __unicode__(self):
        return self.baseuser.username

    def __str__(self):
        return self.baseuser.username
    
    def getPicture(self):
        if self.picture:
            return self.picture.url
    
    def save(self, *args, **kwargs):
        try:
            this_record = UserExtraFields.objects.get(pk=self.pk)
            if this_record.picture != self.picture:
                if "default_profile.jpg" not in this_record.picture.path:
                    this_record.picture.delete(save = False)
        except ValueError:
            pass
        except ObjectDoesNotExist:
            pass #UserExtraFields.objects.create(baseuser=self.baseuser)
        super(UserExtraFields, self).save(*args, **kwargs)
    
    #def delete(self, *args, **kwargs):
    #    super(UserExtraFields, self).delete(*args,**kwargs)


@receiver(post_delete, sender=UserExtraFields)
def post_delete_handler(sender, **kwargs):
    userextrafields = kwargs['instance']
    try:
        storage, path = userextrafields.picture.storage, userextrafields.picture.path
        if "default_profile.jpg" not in userextrafields.picture.path:
            storage.delete(path)
    except ValueError: pass
