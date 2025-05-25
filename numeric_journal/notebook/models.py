from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.postgres.search import SearchVectorField

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Notebook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    notebook = models.ForeignKey(Notebook, null=True, blank=True, on_delete=models.SET_NULL, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    #search_vector = SearchVectorField(null=True, blank=True)  
    note_type = models.CharField(max_length=50, choices=[('text', 'Texte'), ('checklist', 'Checklist')], default='text')
    is_favorite = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField('Tag', related_name='notes', blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.color})"

class NoteVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version de {self.note.title} le {self.created_at}"

class NoteShare(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    permission = models.CharField(max_length=20, choices=[('read', 'Lecture seule'), ('write', 'Lecture/écriture')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.note.title} ({self.permission})"
