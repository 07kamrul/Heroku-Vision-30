from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .form import *

from django.contrib import messages

import datetime
from datetime import date, datetime, timedelta

from django.contrib.sessions.models import Session

Session.objects.all().delete()


# All User


def depositeFeed(request):
    deposit = Deposite.objects.all()

    deposit_posts = sorted(deposit, key=attrgetter('date'), reverse=True)

    context = {'deposit_posts': deposit_posts}

    return render(request, 'accounts/deposite_feed.html', context)


def createDeposite(request):
    form = DepositeForm()

    if request.method == 'POST':
        form = DepositeForm(request.POST)

        if form.is_valid():
            form.save()
            # return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/create_deposite.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allUser(request):
    user = User.objects.all()
    print(user)
    context = {'user': user}
    return render(request, 'accounts/all_users.html', context)


# Register
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            user = authenticate(request, username=username, first_name=first_name, last_name=last_name,
                                email=email, password1=password1, password2=password2)

            # username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='members')
            # user.groups.add(group)
            # Profile.objects.create(
            #     user = user,
            #     first_name = user.first_name,
            #     last_name = user.last_name,
            #     email = user.email,
            # )

            # messages.success(request, 'Account was created for' + user)

            # return redirect('all_user')

            # return redirect('create_profile')
            return redirect('members')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('all_user')

    context = {'form': form}
    return render(request, 'accounts/updateUser.html', context)


# Login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)
    # return render(request, 'accounts/Regilogin.html', context)


# Logout
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def yourProfile(request):
    pro = Profile.objects.filter(user=request.user).values('id')

    if pro:
        for p in pro:
            val = p
            for x in val.values():
                profile = Profile.objects.get(id=x)
                amountprofile = profile.amount_set.all()
                total_amount = sum([item.amount for item in amountprofile])
                pending = amountprofile.filter(status='Pending')
                complete_count = amountprofile.filter(status='Complete').count()

                total_pending = amountprofile.filter(status='Pending').count()

                if pending:
                    total_pending_amount = sum([item.amount for item in pending])
                else:
                    total_pending_amount = 0

                total_complete_amount = total_amount - total_pending_amount

                context = {'profile': profile, 'total_pending_amount': total_pending_amount,
                           'total_complete_amount': total_complete_amount, 'total_pending': total_pending,
                           'complete_count': complete_count}
    else:
        return redirect("/")

    return render(request, 'accounts/profile.html', context)


# Dashboard
@login_required(login_url='login')
def home(request):
    profile = Profile.objects.all()
    gallery = Gallery.objects.all().order_by('-id').reverse()[:10]
    amount = Amount.objects.all().order_by('date').reverse()
    about_us = AboutUs.objects.all().order_by('-id')[:3][::-1]
    last_amount = Amount.objects.all().order_by('date').reverse()[:30]
    vision = Vision.objects.all().order_by('-id')[:5][::-1]
    transCondition = TermsConditions.objects.all().order_by('-id')[:5][::-1]
    notice = Notice.objects.all()

    total_member = profile.count()
    pending = amount.filter(status='Pending')
    pendingCount = amount.filter(status='Pending').count()
    total_pending_amount = sum([item.amount for item in pending])

    complete = amount.filter(status='Complete')
    completeCount = amount.filter(status='Complete').count()
    total_complete_amount = sum([item.amount for item in complete])

    total_amount = sum([item.amount for item in amount])

    pendingAmountFunction = pendingAmounts(request)

    context = {'profile': profile, 'total_amount': total_amount, 'total_member': total_member, 'amount': amount,
               'total_complete_amount': total_complete_amount, 'total_pending_amount': total_pending_amount,
               'completeCount': completeCount, 'pendingCount': pendingCount, 'last_amount': last_amount,
               'gallery': gallery, 'notice': notice, 'pendingAmountFunction': pendingAmountFunction,
               'about_us': about_us, 'vision': vision, 'transCondition': transCondition}

    return render(request, 'accounts/dashboard.html', context)


# Individual Profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profile(request, pk_test):
    profile = Profile.objects.get(id=pk_test)

    # total_amount = profile.amount_set.aggregate(amount=Sum('amount'))

    amountprofile = profile.amount_set.all()

    total_amount = sum([item.amount for item in amountprofile])

    pending = amountprofile.filter(status='Pending')
    complete_count = amountprofile.filter(status='Complete').count()

    total_pending = amountprofile.filter(status='Pending').count()

    if pending:
        total_pending_amount = sum([item.amount for item in pending])
    else:
        total_pending_amount = 0

    total_complete_amount = total_amount - total_pending_amount

    context = {'profile': profile, 'total_pending_amount': total_pending_amount,
               'total_complete_amount': total_complete_amount, 'total_pending': total_pending,
               'complete_count': complete_count}

    return render(request, 'accounts/profile.html', context)


# All Member's Amounts History
@login_required(login_url='login')
def amounts(request):
    profile = Profile.objects.all()

    total_member = profile.count()

    amount = Amount.objects.all().order_by('date').reverse()

    pending = amount.filter(status='Pending')
    pendingCount = amount.filter(status='Pending').count()
    total_pending_amount = sum([item.amount for item in pending])

    complete = amount.filter(status='Complete')
    completeCount = amount.filter(status='Complete').count()
    total_complete_amount = sum([item.amount for item in complete])

    total_amount = sum([item.amount for item in amount])

    context = {'profile': profile, 'total_amount': total_amount, 'total_member': total_member, 'amount': amount,
               'total_complete_amount': total_complete_amount, 'total_pending_amount': total_pending_amount,
               'completeCount': completeCount, 'pendingCount': pendingCount}

    return render(request, 'accounts/amounts.html', context)


# Pending Amount History
@login_required(login_url='login')
def pendingAmounts(request):
    profile = Profile.objects.all()

    amount = Amount.objects.all().order_by('date').reverse()

    pending = amount.filter(status='Pending')

    total_pending = amount.filter(status='Pending').count()

    if pending:
        total_pending_amount = sum([item.amount for item in pending])
        pending_profile = amount.count()

        context = {'profile': profile, 'total_pending_amount': total_pending_amount, 'total_pending': total_pending,
                   'pending_profile': pending_profile, 'amount': amount}

        return render(request, 'accounts/pending_amount.html', context)


# Individual Amounts History
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def individualAmounts(request, pk):
    profile = Profile.objects.get(id=pk)

    # total_amount = profile.amount_set.aggregate(amount=Sum('amount'))

    amountprofile = profile.amount_set.all().order_by('date').reverse()

    total_amount = sum([item.amount for item in amountprofile])

    context = {'profile': profile, 'total_amount': total_amount, 'amountprofile': amountprofile}

    return render(request, 'accounts/individualAmount.html', context)


# Individual Pending Amount History
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def individualPendingAmounts(request, pk):
    profile = Profile.objects.get(id=pk)

    # total_amount = profile.amount_set.aggregate(amount=Sum('amount'))

    amountprofile = profile.amount_set.all().order_by('date').reverse()

    total_pending_count = amountprofile.filter(status='Pending').count()
    pending = amountprofile.filter(status='Pending')

    total_pending_amount = 0
    pending_profile = 0

    if pending:
        total_pending_amount = sum([item.amount for item in pending])

    else:
        total_pending_amount = 0

    context = {'profile': profile, 'total_pending_amount': total_pending_amount, 'amountprofile': amountprofile,
               'total_pending_count': total_pending_count}

    return render(request, 'accounts/individual_pending_amount.html', context)


# Individual Complete Amount History
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def individualCompleteAmounts(request, pk):
    profile = Profile.objects.get(id=pk)

    # total_amount = profile.amount_set.aggregate(amount=Sum('amount'))

    amountprofile = profile.amount_set.all().order_by('date').reverse()

    total_complete_count = amountprofile.filter(status='Complete').count()

    complete = amountprofile.filter(status='Complete')

    if complete:
        total_complete_amount = sum([item.amount for item in complete])

    else:
        total_complete_amount = 0

    context = {'profile': profile, 'total_complete_amount': total_complete_amount, 'amountprofile': amountprofile,
               'total_complete_count': total_complete_count}

    return render(request, 'accounts/individual_complete_amount.html', context)


# Member History
@login_required(login_url='login')
def members(request):
    profile = Profile.objects.all()
    total_member = profile.count()

    pro = Profile.objects.values_list('id')

    habijabi = []

    for i in pro:
        for j in i:
            p = Profile.objects.get(id=j)

            profile_id = j
            name = p.name
            phone = p.phone
            joining_date = p.joining_date
            profile_pic = p.profile_pic

            amounts = p.amount_set.all()
            total_amount = sum([item.amount for item in amounts])

            pending = amounts.filter(status='Pending')
            total_pending = sum([item.amount for item in pending])

            complete = amounts.filter(status='Complete')
            total_complete = sum([item.amount for item in complete])

            total_pending_count = amounts.filter(status='Pending').count()

            context = {'profile': profile, 'profile_id': profile_id, 'name': name, 'joining_date': joining_date,
                       'phone': phone, 'total_pending_count': total_pending_count, 'total_pending': total_pending,
                       'total_complete': total_complete, 'id': i, 'profile_pic': profile_pic}

            habijabi.append(context)

    print(habijabi)
    return render(request, 'accounts/members.html', {'profile_list': habijabi, 'total_member': total_member})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProfile(request):
    form = CreateProfileForm()

    if request.method == 'POST':
        form = CreateProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('members')

    context = {'form': form}
    return render(request, 'accounts/create_profile.html', context)


@login_required(login_url='login')
def updateProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('your_profile')

    context = {'form': form}
    return render(request, 'accounts/update_profile.html', context)


@login_required(login_url='login')
def updatePersonalInformation(request, pk):
    profile = Profile.objects.get(id=pk)
    form = PersonalInformationForm(instance=profile)

    if request.method == 'POST':
        form = PersonalInformationForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('your_profile')

    context = {'form': form}
    return render(request, 'accounts/personal_information_update.html', context)


@login_required(login_url='login')
def updateNomineeInformation(request, pk):
    profile = Profile.objects.get(id=pk)
    form = NomineeInformationForm(instance=profile)

    if request.method == 'POST':
        form = NomineeInformationForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('your_profile')

    context = {'form': form}
    return render(request, 'accounts/nominee_information_update.html', context)


@login_required(login_url='login')
def updatebankinformation(request, pk):
    profile = Profile.objects.get(id=pk)
    form = BankInformationForm(instance=profile)

    if request.method == 'POST':
        form = BankInformationForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('your_profile')

    context = {'form': form}
    return render(request, 'accounts/bank_information_update.html', context)


@login_required(login_url='login')
def accountSettings(request, pk):
    profile = Profile.objects.get(id=pk)

    form = PictureForm(instance=profile)
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('your_profile')

    context = {'form': form}

    return render(request, 'accounts/settings.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createAmount(request):
    form = CreateAmountForm()

    if request.method == 'POST':
        form = CreateAmountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added!")
            return redirect('amounts')
        else:
            messages.error(request, "Please fill in all the fields.")

    context = {'form': form}

    return render(request, 'accounts/create_amount.html', context)


@login_required(login_url='login')
def viewAmount(request, pk):
    amount = Amount.objects.get(id=pk)
    form = AmountForm(instance=amount)

    if request.method == 'POST':
        form = AmountForm(request.POST, request.FILES, instance=amount)

        if form.is_valid():
            form.save()
            return redirect('amounts')

    context = {'form': form, 'amount': amount}

    return render(request, 'accounts/view_amount.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateAmount(request, pk):
    amount = Amount.objects.get(id=pk)

    form = AmountForm(instance=amount)
    if request.method == 'POST':
        form = AmountForm(request.POST, request.FILES, instance=amount)

        if form.is_valid():
            form.save()
            return redirect('amounts')

    context = {'form': form, 'amount': amount}

    return render(request, 'accounts/update_amount.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAmount(request, pk):
    amount = Amount.objects.get(id=pk)

    if request.method == 'POST':
        amount.delete()
        return redirect('amounts')

    context = {'amount': amount}

    return render(request, 'accounts/delete_amount.html', context)


@login_required(login_url='login')
def settings(request):
    context = {}
    return render(request, 'accounts/settings.html', context)


@login_required(login_url='login')
def userProfile(request):
    context = {}
    return render(request, 'accounts/user_profile.html', context)


@login_required(login_url='login')
def totalCost(request):
    cost = TotalCost.objects.all()

    total_cost = sum([item.amount for item in cost])

    context = {'cost': cost, 'total_cost': total_cost}

    return render(request, 'accounts/total_cost.html', context)


@login_required(login_url='login')
def aboutUs(request):
    aboutUs = AboutUs.objects.all()
    context = {'aboutUs': aboutUs}

    return render(request, 'accounts/about_us/about_us.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createAboutUs(request):
    form = AboutUsForm()

    if request.method == 'POST':
        form = AboutUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about_us')

    context = {'form': form}

    return render(request, 'accounts/about_us/create_about_us.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editAboutUs(request, pk):
    aboutUs = AboutUs.objects.get(id=pk)
    form = AboutUsForm(instance=aboutUs)

    if request.method == 'POST':
        form = AboutUsForm(request.POST, instance=aboutUs)

        if form.is_valid():
            form.save()
            return redirect('about_us')

    context = {'form': form, 'aboutUs': aboutUs}

    return render(request, 'accounts/about_us/edit_about_us.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAboutUs(request, pk):
    aboutUs = AboutUs.objects.get(id=pk)

    if request.method == 'POST':
        aboutUs.delete()
        return redirect('about_us')

    context = {'aboutUs': aboutUs}

    return render(request, 'accounts/about_us/delete_about_us.html', context)


@login_required(login_url='login')
def vision(request):
    vision = Vision.objects.all()
    context = {'vision': vision}

    return render(request, 'accounts/vision/vision.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createVision(request):
    form = VisionForm()

    if request.method == 'POST':
        form = VisionForm(request.POST)
        if form.is_valid():
            create_vision = form.save()
            vision = form.cleaned_data.get('vision')
            create_vision = authenticate(request, vision=vision)
            return redirect('vision')

    context = {'form': form}
    return render(request, 'accounts/vision/create_vision.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editVision(request, pk):
    vision = Vision.objects.get(id=pk)
    form = VisionForm(instance=vision)

    if request.method == 'POST':
        form = VisionForm(request.POST, instance=vision)

        if form.is_valid():
            form.save()
            return redirect('vision')

    context = {'form': form, 'vision': vision}
    return render(request, 'accounts/vision/edit_vision.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteVision(request, pk):
    vision = Vision.objects.get(id=pk)

    if request.method == 'POST':
        vision.delete()
        return redirect('vision')

    context = {'vision': vision}

    return render(request, 'accounts/vision/delete_vision.html', context)


@login_required(login_url='login')
def termsConditions(request):
    termsConditions = TermsConditions.objects.all()
    context = {'termsConditions': termsConditions}

    return render(request, 'accounts/terms_conditions/terms_conditions.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createTermsConditions(request):
    form = TermsConditionsForm()

    if request.method == 'POST':
        form = TermsConditionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('terms_conditions')

    context = {'form': form}
    return render(request, 'accounts/terms_conditions/create_terms_conditions.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTermsConditions(request, pk):
    termsConditions = TermsConditions.objects.get(id=pk)

    form = TermsConditionsForm(instance=termsConditions)

    if request.method == 'POST':
        form = VisionForm(request.POST, instance=termsConditions)

        if form.is_valid():
            form.save()
            return redirect('terms_conditions')

    context = {'form': form}

    return render(request, 'accounts/terms_conditions/edit_terms_conditions.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteTermsConditions(request, pk):
    termsConditions = TermsConditions.objects.get(id=pk)

    if request.method == 'POST':
        termsConditions.delete()
        return redirect('terms_conditions')

    context = {'termsConditions': termsConditions}

    return render(request, 'accounts/terms_conditions/delete_terms_conditions.html', context)


@login_required(login_url='login')
def gallery(request):
    gallery = Gallery.objects.all()
    context = {'gallery': gallery}

    return render(request, 'accounts/gallery/gallery.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createGallery(request):
    form = GalleryForm()

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added!")
            return redirect('gallery')
        else:
            messages.error(request, "Please fill in all the fields.")

    context = {'form': form}

    return render(request, 'accounts/gallery/create_gallery.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editGallery(request, pk):
    gallery = Gallery.objects.get(id=pk)
    form = GalleryForm(instance=gallery)

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)

        if form.is_valid():
            form.save()
            return redirect('gallery')

    context = {'form': form}

    return render(request, 'accounts/gallery/edit_gallery.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteGallery(request, pk):
    gallery = Gallery.objects.get(id=pk)

    if request.method == 'POST':
        gallery.delete()
        return redirect('gallery')

    context = {'gallery': gallery}

    return render(request, 'accounts/gallery/delete_gallery.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createSlider(request):
    gallery = Gallery.objects.all()
    context = {'gallery': gallery}

    return render(request, 'accounts/gallery/create_slider.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteSlider(request):
    slider = Slider.objects.all()
    context = {'slider': slider}

    return render(request, 'accounts/gallery/delete_slider.html', context)


@login_required(login_url='login')
def notice(request):
    notice = Notice.objects.all()
    context = {'notice': notice}

    return render(request, 'accounts/notice/notice.html', context)


@login_required(login_url='login')
def singleNotice(request, pk):
    notice = Notice.objects.get(id=pk)
    context = {'notice': notice}

    return render(request, 'accounts/notice/single_notice.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createNotice(request):
    form = NoticeForm()

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added!")
            return redirect('notice')
        else:
            messages.error(request, "Please fill in all the fields.")

    context = {'form': form}

    return render(request, 'accounts/notice/create_notice.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editNotice(request, pk):
    notice = Notice.objects.get(id=pk)
    form = NoticeForm(instance=notice)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)

        if form.is_valid():
            form.save()
            return redirect('notice')

    context = {'form': form}

    return render(request, 'accounts/notice/edit_notice.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteNotice(request, pk):
    notice = Notice.objects.get(id=pk)

    if request.method == 'POST':
        notice.delete()
        return redirect('notice')

    context = {'notice': notice}

    return render(request, 'accounts/notice/delete_notice.html', context)
