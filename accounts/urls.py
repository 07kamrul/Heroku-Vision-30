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

    # About Us
    # --------------------------------------------------------------------
    path('about_us/', views.aboutUs, name="about_us"),
    path('create_about_us/', views.createAboutUs, name="create_about_us"),
    path('edit_about_us/<str:pk>/', views.editAboutUs, name="edit_about_us"),
    path('delete_about_us/<str:pk>/', views.deleteAboutUs, name="delete_about_us"),
    # --------------------------------------------------------------------

    # Vision
    # --------------------------------------------------------------------
    path('vision/', views.vision, name="vision"),
    path('create_vision/', views.createVision, name="create_vision"),
    path('edit_vision/<str:pk>/', views.editVision, name="edit_vision"),
    path('delete_vision/<str:pk>/', views.deleteVision, name="delete_vision"),
    # --------------------------------------------------------------------

    # Terms and Conditions
    # --------------------------------------------------------------------
    path('terms_conditions/', views.termsConditions, name="terms_conditions"),
    path('create_terms_conditions/', views.createTermsConditions, name="create_terms_conditions"),
    path('edit_terms_conditions/<str:pk>/', views.editTermsConditions, name="edit_terms_conditions"),
    path('delete_terms_conditions/<str:pk>/', views.deleteTermsConditions, name="delete_terms_conditions"),
    # --------------------------------------------------------------------

    # Gallery
    # --------------------------------------------------------------------
    path('gallery/', views.gallery, name="gallery"),
    path('create_gallery/', views.createGallery, name="create_gallery"),
    path('edit_gallery/<str:pk>/', views.editGallery, name="edit_gallery"),
    path('delete_gallery/<str:pk>/', views.deleteGallery, name="delete_gallery"),
    # --------------------------------------------------------------------

    # Slider
    # --------------------------------------------------------------------
    path('create_slider/', views.createSlider, name="create_slider"),
    path('delete_slider/<str:pk>/', views.deleteSlider, name="delete_slider"),
    # --------------------------------------------------------------------

    # Notice
    # --------------------------------------------------------------------
    path('notice/', views.notice, name="notice"),
    path('single_notice/<str:pk>/', views.singleNotice, name="single_notice"),
    path('create_notice/', views.createNotice, name="create_notice"),
    path('edit_notice/<str:pk>/', views.editNotice, name="edit_notice"),
    path('delete_notice/<str:pk>/', views.deleteNotice, name="delete_notice"),
    # --------------------------------------------------------------------

]
