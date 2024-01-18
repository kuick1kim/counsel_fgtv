from django.urls import path

from posts.views import *
# (*
#     feeds,
#     comment_add,
#     comment_delete,
#     post_add,
#     tags,
#     post_detail,
#     post_like,
#     post_delete,
# )

app_name = "posts"
urlpatterns = [

    # path("comments/<int:comment_id>/delete/", comment_delete, name="comment_delete"),
    # path("post_add/", post_add, name="post_add"),
    # path("<int:post_id>/", post_detail, name="post_detail"),
    # path("post/<int:post_id>/delete/", post_delete, name="post_delete"),    
    # path("comment_add/", comment_add2, name="comment_add2"),


    path("feeds/", feeds2, name="feeds"),
    path("tags/<str:tag_name>/", tags, name="tags"),
    path("tags/<str:tag_name>/", tags2, name="tags2"),
    path("<int:post2_id>/", post_detail2, name="post_detail2"),
    path("comment_add/", comment_add, name="comment_add"),
    path("comment_addtag/", comment_addtag, name="comment_addtag"),

    path("<int:post2_id>/like/", post_like2, name="post_like2"),
    path("post_add/", post_add, name="post_add"),
    
    path("post_add2/", post_add2, name="post_add2"),
    path("comments/<int:comment_id>/delete/", comment_delete2, name="comment_delete2"),

    path('text_entry_list/', text_entry_list, name='text_entry_list'),
    path("admin1/aa/", admin1, name="admin1"),
    path("date_range_view/delete_row/<int:row_id>", delete_row, name="delete_row"),
    path("admin1/aa/delete_row/<int:row_id>", delete_row, name="delete_row"),

    path("admin2/delete_row2/<int:row_id>", delete_row2, name="delete_row2"),
    path("admin2/", admin2, name="admin2"),
    path('create/', create_text_entry, name='create_text_entry'),
    
    path('admin1/aa/', date_range_view, name='date_range_view'),
    path('download_csv/', download_csv, name='download_csv'), #### 추가한다. 
]
