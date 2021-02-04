from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('follows/', views.FollowsView.as_view(), name='follows'),
    path('search/', views.search, name='search'),
    path('searchresults/<str:searchterm>/', views.search_results, name='searchresults'),
    path('searchresults/posts/<str:searchterm>/', views.MoreSearchPosts.as_view(), name='postssearchresults'),
    path('searchresults/users/<str:searchterm>/', views.MoreSearchUsers.as_view(), name='userssearchresults'),
    path('staff/addcategory/', views.add_category, name='addcategory'),
    path('staff/editcategory/<int:category_id>/', views.edit_category, name='editcategory'),
    path('staff/deletecategory/<int:category_id>/', views.delete_category, name='deletecategory'),
    path('staff/carouselsettings', views.carousel_settings, name='carouselsettings'),
    path('staff/editcarousel/<int:carousel_id>/', views.edit_carousel, name='editcarousel'),
    path('category/<str:category_title>/', views.Fullcategory.as_view(), name='fullcategory'),
    path('profile/<int:author_id>/', views.Profile.as_view(), name='profile'),
    path('profile/myprofile/', views.MyProfile.as_view(), name='myprofile'),
    path('createpost/', views.create_post, name='createpost'),
    path('post/<int:post_id>/', views.fullpost, name='fullpost'),
    path('editpost/<int:post_id>/', views.update_post, name='editpost'),
    path('likepost/<int:post_id>/', views.likepost, name='likepost'),
    path('followprofile/<int:profile_id>/', views.followprofile, name='followprofile'),
    path('likedposts/', views.Favposts.as_view(), name='likedposts'),
    path('likecomment/<int:comment_id>/', views.likecomment, name='likecomment'),
    path('likereply/<int:reply_id>/', views.likereply, name='likereply'),
    path('staff/', views.staff_Settings, name='staff'),
    path('staff/categorysettings', views.category_settings, name='categorysettings'),
    #path('staff/addcarousel/', views.add_carousel, name='addcarousel'),
    #path('staff/deletecarousel/<int:carousel_id>/', views.delete_carousel, name='deletecarousel'),
]

