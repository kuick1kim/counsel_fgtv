from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True, null=True)    
    first_name = models.CharField(max_length=30, blank=False, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=True)

    like_posts = models.ManyToManyField(
        "posts.Post2",    verbose_name="좋아요 누른 Post목록",
        related_name="like_users",  blank=True,
    )
    following = models.ManyToManyField(
        "self",      verbose_name="팔로우 중인 사용자들",
        related_name="followers",       symmetrical=False,
        through="users.Relationship",
    )

    def __str__(self):
        return self.username











class Relationship(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우를 요청한 사용자",
        related_name="following_relationships",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 요청의 대상",
        related_name="follower_relationships",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"관계 ({self.from_user} -> {self.to_user})"
