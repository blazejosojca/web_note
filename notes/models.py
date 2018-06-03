from django.db import models
from django.contrib.auth.models import User


# Topic of the note
class Topic(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # using model User to connect Topic with owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Entries for topics
class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry_text = models.TextField()
    entry_date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        if len(self.entry_text) > 50:
            text = self.entry_text[:50] + " ..."
        else:
            text = self.entry_text
        return text
