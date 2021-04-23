from django.urls import path
from . import views

urlpatterns = [

    # User
    # --------------------------------------------------------------------
    path('updateUser/<str:pk>/', views.updateUser, name="updateUser"),
    path('all_user/', views.allUser, name="all_user"),
    path('user_profile/', views.userProfile, name="user_profile"),
    # --------------------------------------------------------------------
    # Sign in Sign up
    # --------------------------------------------------------------------
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # --------------------------------------------------------------------
    # Profile
    # --------------------------------------------------------------------
    path('profile/<str:pk_test>/', views.profile, name="profile"),
    path('create_profile/', views.createProfile, name="create_profile"),
    path('update_profile/<str:pk>/', views.updateProfile, name="update_profile"),
    # --------------------------------------------------------------------
    # Individual Profile
    # --------------------------------------------------------------------
    path('your_profile/', views.yourProfile, name="your_profile"),
    path('personal_information_update/<str:pk>/', views.updatePersonalInformation, name="personal_information_update"),
    path('nominee_information_update/<str:pk>/', views.updateNomineeInformation, name="nominee_information_update"),
    path('bank_information_update/<str:pk>/', views.updatebankinformation, name="bank_information_update"),
    # --------------------------------------------------------------------
    # Amount
    # --------------------------------------------------------------------
    path('amounts/', views.amounts, name="amounts"),
    path('pending_amount/', views.pendingAmounts, name="pending_amount"),
    path('create_amount/', views.createAmount, name="create_amount"),
    path('view_amount/<str:pk>/', views.viewAmount, name="view_amount"),
    path('update_amount/<str:pk>/', views.updateAmount, name="update_amount"),
    path('delete_amount/<str:pk>/', views.deleteAmount, name="delete_amount"),
    # --------------------------------------------------------------------
    # Individual Amount
    # --------------------------------------------------------------------
    path('individual_amount/<str:pk>/', views.individualAmounts, name="individual_amount"),
    path('individual_pending_amount/<str:pk>/', views.individualPendingAmounts, name="individual_pending_amount"),
    path('individual_complete_amount/<str:pk>/', views.individualCompleteAmounts, name="individual_complete_amount"),
    # --------------------------------------------------------------------
    # Members
    # --------------------------------------------------------------------
    path('members/', views.members, name="members"),
    # --------------------------------------------------------------------
    # Feeds
    # --------------------------------------------------------------------
    path('depositFeed/', views.depositeFeed, name="depositeFeed"),
    path('create_deposite/', views.createDeposite, name="create_deposite"),
    # --------------------------------------------------------------------
    #Total Cost
    # --------------------------------------------------------------------
    path('total_cost/', views.totalCost, name="total_cost"),
    # --------------------------------------------------------------------


    path('', views.home, name="home"),

    path('settings/<str:pk>/', views.accountSettings, name="settings"),

]
