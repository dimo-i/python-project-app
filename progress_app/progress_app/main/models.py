from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


UserModel = get_user_model()


#TODO DEFAULT VALUES

class Category(models.Model):
    NAME_MAX_LENGTH = 50
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        db_index=True,
    )


    category_image = models.URLField()

    category_description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


#TODO DEFAULT VALUES

class Project(models.Model):
    MIN_LENGTH = 5
    NAME_MAX_LENGTH = 100
    RELATED_NAME = 'projects'

    category = models.ForeignKey(
        Category,
        related_name=RELATED_NAME,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(MIN_LENGTH),
        ),
    )

    project_image = models.ImageField()


    description = models.TextField(
        blank=True,
        validators=(
            MinLengthValidator(MIN_LENGTH),
        ),
    )
    post_date = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.PROTECT,
    )

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-post_date',)


    def __str__(self):
        return self.name

##########

class ProjectAlbum(models.Model):
    IMG_DESCRIPTION_MIN_LENGTH = 5
    IMAGE_DESC_MAX_LENGTH = 300
    DEFAULT_UPLOAD_TO = 'images/'

    project = models.ForeignKey(
        Project,
        default=None,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        default=None,
        on_delete=models.CASCADE,
    )

    album_image = models.ImageField(
        upload_to=DEFAULT_UPLOAD_TO
    )

    image_description = models.CharField(
        max_length=IMAGE_DESC_MAX_LENGTH,
        validators=(
            MinLengthValidator(IMG_DESCRIPTION_MIN_LENGTH),
        ),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.project.name
