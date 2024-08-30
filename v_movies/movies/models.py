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
    
    def get_full_name(self):
        return f"{self.name} {self.last_name}"


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
    
class AbstractFilm(models.Model):
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

    # Title is persian_title 
    title = models.CharField(max_length=350, verbose_name="نام فارسی")
    english_title = models.CharField(max_length=350, verbose_name="نام انگلیسی")
    year_of_manufacture = models.IntegerField(verbose_name="سال ساخت")
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    country = models.CharField(
        max_length=30, choices=MADE_IN_CHOICES, verbose_name="کشور سازنده"
    )
    legal_age = models.PositiveIntegerField(verbose_name="سن قانونی")
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
    is_perimium = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, verbose_name="ژانر ها")
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def get_actors(self):
        return ", ".join([actor.name for actor in self.actors.all()])

    get_actors.short_description = "بازیگران"

    def get_genres(self):
        return ", ".join([genre.title for genre in self.genres.all()])

    get_genres.short_description = "ژانر ها"

    def updateLikes(self):
        self.likes += 1
        self.save()


class Movie(AbstractFilm):
    duraction = models.PositiveIntegerField(
        null=True, verbose_name="زمان ویدیو به دقیقه"
    )
    videofile = models.FileField(
        upload_to="video", null=True, blank=True, verbose_name="ویدیو ی فیلم"
    )
    download_link_480 = models.CharField(max_length=80, null=True, verbose_name="لینک دانلود با کیفیت 480")
    download_link_720 = models.CharField(max_length=80, null=True, verbose_name="لینک دانلود با کیفیت 720")
    download_link_1080 = models.CharField(max_length=80, null=True, verbose_name="لینک دانلود با کیفیت 1080")

    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "movies:movie_detail",
            kwargs={
                "slug": self.slug,
            },
        )


class Serial(AbstractFilm):
    episodes_number = models.PositiveIntegerField(default=0)
    seasons = models.PositiveIntegerField(default=1, verbose_name="فصل ها")
    is_perimium = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "سریال"
        verbose_name_plural = "سریال ها"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            "movies:serial_detail",
            kwargs={
                "slug": self.slug,
            },
        )


class SerialEpisode(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان قسمت")
    number_of_episode = models.IntegerField(verbose_name="قسمت چندم")
    videofile = models.FileField(
        upload_to="video", null=True, blank=True, verbose_name="ویدیو ی این قسمت"
    )
    download_link_480 = models.CharField(max_length=80, verbose_name="لینک دانلود با کیفیت 480")
    download_link_720 = models.CharField(max_length=80, verbose_name="لینک دانلود با کیفیت 720")
    download_link_1080 = models.CharField(max_length=80, verbose_name="لینک دانلود با کیفیت 1080")
    season = models.PositiveIntegerField(verbose_name="فصل")

    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated = models.DateTimeField(auto_now=True)

    serial = models.ForeignKey(Serial, on_delete=models.PROTECT, related_name="episodes")

    class Meta:
        ordering = ["number_of_episode"]
        verbose_name = "قسمت سریال"
        verbose_name_plural = "قسمت های سریال"

    def __str__(self):
        return self.title
    

class AbstractComment(models.Model):
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class MovieComments(AbstractComment):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "نظر فیلم سینمایی ها"
        verbose_name_plural = "نظرات فیلم سینمایی ها"

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

class SerialComments(AbstractComment):
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "نظر سریال ها"
        verbose_name_plural = "نظرات سریال ها"

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
