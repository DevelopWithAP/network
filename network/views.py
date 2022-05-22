from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse


from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-created_on")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, 5)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.method == "POST":
        author = request.user
        content = request.POST["content"]
        Post.objects.create(author=author, content=content)
        context = {
            "page_obj": page_obj,
        }
        return render(request, "network/index.html", context)
    return render(request, "network/index.html", {"page_obj": page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    num_followers = user.count_followers()
    num_following = user.count_following()

    posts = Post.objects.filter(author=user)
    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, 2)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "user": user,
        "followers": num_followers,
        "following": num_following,
        "page_obj": page_obj
    }
    return render(request, "network/profile.html", context)


@csrf_exempt
@login_required
def follow(request):
    if request.method == "POST":
        user_id = int(request.POST.get("user_id"))
        follower_id = int(request.POST.get("follower_id"))
        action = request.POST["action"]

        user = User.objects.get(pk=user_id)
        follower = User.objects.get(pk=follower_id)

        if action == "Follow":
            user.followers.add(follower)
            user.save()
            return JsonResponse({
                "status": 201,
                "action": "Following",
                "followers": user.count_followers()
            })
        elif action == "Following":
            user.followers.remove(follower)
            user.save()
            return JsonResponse({
                "status": 201,
                "action": "Follow",
                "followers": user.count_followers()
            })
    return JsonResponse({"message": "Method not allowed"}, status=403)


@login_required
def following(request):
    if request.method == "GET":
        user = request.user
        following = user.get_following()

        posts = Post.objects.filter(author__in=following)

        context = {
            "posts": posts
        }
        return render(request, "network/following.html", context)


@login_required
@csrf_exempt
def edit(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": f"Could not find post with id {post_id}"}, status=400)

        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data.get("content")
            post.edited = True
            post.save()

            data = {
                "content": post.content,
                "edited": "true"
            }
            return JsonResponse(data, status=200)
    return JsonResponse({"message": "Method not allowed"}, status=403)


@login_required
@csrf_exempt
def like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Could not find post with id {post_id}"}, status=400)
    if request.method == "POST":
        data = json.loads(request.body)

        if data.get("post_id") is not None and data.get("action") is not None:
            if data.get("action") == "like":
                post.likes.add(request.user)
                post.save()
                return JsonResponse({
                    "action": "unlike",
                    "likes": post.get_likes()
                })
            elif data.get("action") == "unlike":
                post.likes.remove(request.user)
                post.save()
                return JsonResponse({
                    "action": "like",
                    "likes": post.get_likes()
                })
        return JsonResponse({"error": "Bad Request"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=403)


@csrf_exempt
@login_required
def toggle_visibility(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Cound not find post with id {post_id}"})
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = int(data["post_id"])
        post = Post.objects.get(pk=post_id)
        print(data)
        if data.get("post_id") is not None:
            if data.get("action") == "remove":
                post.is_visible = False
                post.save()
                return JsonResponse({"message": f"Post {post_id} no longer visible"}, status=200)
        return JsonResponse({"error": "Bad request"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=403)
