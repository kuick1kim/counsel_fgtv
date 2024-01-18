import admin_thumbnails
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from posts.models import *  #Post, PostImage, Comment,Comment2, HashTag, Post2


admin.site.register(TextEntry_a)
admin.site.register(TextEntry_b)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class CommentInline2(admin.TabularInline):
    model = Comment2
    extra = 1



class InlineImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, "url", None):
            html = mark_safe(f'<img src="{value.url}" width="150" height="150">') + html
        return html

@admin_thumbnails.thumbnail("photo")
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

















@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
        "created",
    ]
    inlines = [
        CommentInline,
        PostImageInline,
        # LikeUserInline,
    ]
    formfield_overrides = {ManyToManyField: {"widget": CheckboxSelectMultiple}}



################################
################################
################################
################################
################################

# class LikeUserInline2(admin.TabularInline):
#     model = Post2.like_users.through
    # verbose_name = "좋아요 한 User"
    # verbose_name_plural = f"{verbose_name} 목록"
    # extra = 1

    # def has_change_permission(self, request, obj=None):
    #     return False


class LikeUserInline(admin.TabularInline):
    model = Post2.like_users.through
    verbose_name = "좋아요 한 User"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False



@admin.register(Post2)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content_a",
        "content_b",
        "content_c",
        "created2",
    ]
    inlines = [
        CommentInline2,
        LikeUserInline,
    ]
    formfield_overrides = {ManyToManyField: {"widget": CheckboxSelectMultiple}}







@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "photo",
    ]







@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "content",
        "created",
    ]


@admin.register(Comment2)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "content",
        "created",
    ]




@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass
