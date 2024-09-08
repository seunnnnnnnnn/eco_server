# from django.urls import path, include
# from . import views
# from rest_framework.routers import DefaultRouter

# # Create a router and register our viewsets with it.



# urlpatterns = [
#     path('auth/token/', views.user_auth, name="login_view"),
#     path("auth/logout/", views.logout_view, name="logout_view"),
#     path('auth/verify/', views.otp_verification),
#     path('teams/create/', views.teams_view),
#     path('teams/join/', views.join_team),
#     path('teams/list/', views.user_teams),
#     path('teams/<uuid:pk>/leave/', views.leave_team),
#     path('teams/<uuid:pk>/delete/', views.delete_team),
#     path('scan/upload/', views.ApproximateImage.as_view()),
#     path('scan/confirm-bin/', views.ConfirmBinView.as_view()),
#     path('scan/list/', views.ScansView.as_view()),
#     path('scans/user/', views.UserStatsView.as_view()),
#     path('leaderboard/', views.LeaderBoard.as_view()),

# ]


from django.urls import path
from . import views

urlpatterns = [
    path('user/auth/', views.user_auth, name='user_auth'),
    path('logout/', views.logout_view, name='logout_view'),
    path('update/firebase/', views.update_firebase_token, name='update_firebase_token'),
    path('reset/otp/', views.reset_otp, name='reset_otp'),
    path('otp/verification/', views.otp_verification, name='otp_verification'),
    path('teams/', views.teams_view, name='teams_view'),
    path('user/teams/', views.user_teams, name='user_teams'),
    path('join/team/', views.join_team, name='join_team'),
    path('leave/team/<uuid:pk>/', views.leave_team, name='leave_team'),  # Changed to UUID
    path('delete/team/<uuid:pk>/', views.delete_team, name='delete_team'),  # Changed to UUID
    path('confirm/bin/', views.ConfirmBinView.as_view(), name='confirm_bin_view'),
    path('approximate/image/', views.ApproximateImage.as_view(), name='approximate_image'),
    path('scans/', views.ScansView.as_view(), name='scans_view'),
    path('user/stats/', views.UserStatsView.as_view(), name='user_stats_view'),
    path('leaderboard/', views.LeaderBoard.as_view(), name='leaderboard'),
]
