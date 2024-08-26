from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse


class Actor(models.Model):
    name = models.CharField(max_length=60, verbose_name="اسم بازیگر")
    last_name = models.CharField(max_length=60, verbose_name="فامیلی بازیگر")
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    position = models.IntegerField()

    class Meta:
        ordering = ("position",)
        verbose_name = "بازیگر"
        verbose_name_plural = "بازیگران"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            "movies:actor_list",
            kwargs={
                "actor_slug": self.slug,
            },
        )


class Genre(models.Model):
    title = models.CharField(max_length=60, verbose_name="اسم ژانر")
    slug = models.CharField(max_length=60)
    position = models.IntegerField()

    class Meta:
        ordering = ("position",)
        verbose_name = "ژانر"
        verbose_name_plural = "ژانر ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "movies:genre_list",
            kwargs={
                "genre_slug": self.slug,
            },
        )


class Film(models.Model):
    MADE_IN_CHOICES = (
        ("ایالات متحده آمریکا", "ایالات متحده آمریکا"),
        ("ایران", "ایران"),
        ("کانادا", "کانادا"),
        ("انگلستان", "انگلستان"),
        ("آلمان", "آلمان"),
        ("فرانسه", "فرانسه"),
        ("ایتالیا", "ایتالیا"),
        ("روسیه", "روسیه"),
        ("چین", "چین"),
        ("ژاپن", "ژاپن"),
        ("هند", "هند"),
        ("برزیل", "برزیل"),
        ("استرالیا", "استرالیا"),
        ("مکزیک", "مکزیک"),
        ("آفریقای جنوبی", "آفریقای جنوبی"),
        ("ترکیه", "ترکیه"),
        ("عربستان سعودی", "عربستان سعودی"),
        ("آرژانتین", "آرژانتین"),
        ("مصر", "مصر"),
        ("اسپانیا", "اسپانیا"),
        ("لهستان", "لهستان"),
        ("هلند", "هلند"),
    )

    # Movie has english and persian name
    title = models.CharField(max_length=350, verbose_name="نام فارسی")
    english_name = models.CharField(max_length=350, verbose_name="نام انگلیسی")
    year_of_manufacture = models.IntegerField(verbose_name="سال ساخت")
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    made_in = models.CharField(
        max_length=30, choices=MADE_IN_CHOICES, verbose_name="کشور سازنده"
    )
    legal_age = models.PositiveIntegerField(verbose_name="سن قانونی")
    film_time = models.PositiveIntegerField(
        null=True, verbose_name="زمان ویدیو به دقیقه"
    )
    score = models.FloatField(max_length=3, verbose_name="امتیاز از ده")
    actors = models.ManyToManyField(Actor, verbose_name="بازیگران")
    story = models.CharField(max_length=500, verbose_name="داستان فیلم")
    about_movie = models.CharField(max_length=500, verbose_name="درباره فیلم")
    thumbnail = models.ImageField(
        upload_to="image", null=True, blank=True, verbose_name="تصویر"
    )
    trailer = models.FileField(
        upload_to="video", null=True, blank=True, verbose_name="تریلر فیلم"
    )
    videofile = models.FileField(
        upload_to="video", null=True, blank=True, verbose_name="ویدیو ی فیلم"
    )
    is_payed = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, verbose_name="ژانر ها")
    tags = TaggableManager()

    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم ها"

    def __str__(self):
        return self.title

    def get_actors(self):
        return ", ".join([actor.name for actor in self.actors.all()])

    get_actors.short_description = "بازیگران"

    def get_genres(self):
        return ", ".join([genre.title for genre in self.genres.all()])

    get_genres.short_description = "ژانر ها"

    def get_absolute_url(self):
        return reverse(
            "movies:post_detail",
            kwargs={
                "slug": self.slug,
            },
        )
    
class Serial(models.Model):
    pass


class Comment(models.Model):
    movie = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
