from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    if 'uid' in request.session:
        return redirect('/wishes')
    return render(request, "login_reg.html")


def process_user(request):
    if request.method == 'POST':
        is_reg = request.POST.get('type')
        if is_reg == 'reg':  # registration
            errors = User.objects.reg_validator(request.POST)
            if len(errors) > 0:
                for key, val in errors.items():
                    messages.error(request, val)
                request.session['is_reg'] = "true"
                return redirect('/')
            else:
                fname = request.POST['fname']
                lname = request.POST['lname']
                email = request.POST['email']
                new_pass = bcrypt.hashpw(
                    request.POST['pass'].encode(), bcrypt.gensalt()).decode()
                new_user = User.objects.create(
                    first_name=fname, last_name=lname, email=email, password=new_pass)
                request.session['uid'] = new_user.id
                return redirect('/wishes')
        else:  # log in
            errors = User.objects.login_validator(request.POST)
            if len(errors) > 0:
                for key, val in errors.items():
                    messages.error(request, val)
                request.session['is_reg'] = "false"
                return redirect('/')
            else:
                # made sure email is unique upon registration
                logged_user = User.objects.get(email=request.POST['email'])
                if bcrypt.checkpw(request.POST['pass'].encode(), logged_user.password.encode()):
                    request.session['uid'] = logged_user.id
                    return redirect('/wishes')
                else:
                    messages.error(request, "Invalid Log in")
                    return redirect('/')


def wishes(request):
    if 'uid' in request.session:
        context = {
            "this_user": User.objects.get(id=request.session['uid']),
            "this_user_wishes":User.objects.get(id=request.session['uid']).wishes.all().order_by('-created_at'),
            "all_granted_wishes": Wish.objects.filter(is_granted=True).order_by('-created_at'),
        }
        return render(request, "wishes.html", context)

    else:
        return redirect("/")


def Add_wish(request):
    if 'uid' in request.session:
        context = {
            "this_user": User.objects.get(id=request.session['uid'])
        }
        return render(request, "add_wish.html", context)
    else:
        return redirect('/')


def create_wish(request):
    if 'uid' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/wishes/new')
        else:
            new_item = request.POST['item']
            new_desc = request.POST['desc']
            this_wisher = User.objects.get(id=request.session['uid'])
            Wish.objects.create(item=new_item, description=new_desc,
                                wisher=this_wisher, is_granted=False)
            return redirect('/wishes')


def grant_wish(request, id):
    if 'uid' not in request.session:
        return redirect('/')

    this_wish = Wish.objects.get(id=id)
    this_wish.is_granted = True
    this_wish.save()
    return redirect("/wishes")


def like_wish(request, id):
    if 'uid' not in request.session:
        return redirect('/')

    this_wish = Wish.objects.get(id=id)
    this_wish.liked_by.add(User.objects.get(id=request.session['uid']))
    return redirect('/wishes')


def edit_wish(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        "this_wish": Wish.objects.get(id=id),
        "this_user": User.objects.get(id=request.session['uid']),
    }
    return render(request, "edit_wish.html", context)


def update_wish(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect(f'/wishes/edit/{id}')
        else:
            updated_item = request.POST['item']
            updated_desc = request.POST['desc']
            wish_to_update = Wish.objects.get(id=id)
            wish_to_update.item = updated_item
            wish_to_update.description = updated_desc
            wish_to_update.save()
            return redirect('/wishes')


def delete_wish(request, id):
    if 'uid' not in request.session:
        return redirect('/')
    wish_to_del = Wish.objects.get(id=id)
    wish_to_del.delete()
    return redirect('/wishes')


def stats(request):
    if 'uid' not in request.session:
        return redirect('/')
    context = {
        "this_user": User.objects.get(id=request.session['uid']),
        "this_user_granted": User.objects.get(id=request.session['uid']).wishes.all().filter(is_granted = True).count,
        "this_user_pending": User.objects.get(id=request.session['uid']).wishes.all().filter(is_granted = False).count,
        "all_granted_wishes": Wish.objects.filter(is_granted = True).count
    }
    return render(request, "stats.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')
