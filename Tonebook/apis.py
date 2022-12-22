from django.http import JsonResponse
import json
from .models import User, File
from datetime import datetime, timezone


def create(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You need to be logged in to create a new file."
        })

    if request.method != "POST":
        return JsonResponse({
            "error": "This method is not allowed"
        })

    body = json.loads(request.body)

    if not body["name"] or len(body["name"]) < 3:
        return JsonResponse({
            "error": "You need to enter a name, minimum 3 characters."
        })

    og_user = User.objects.get(username=request.user.username)

    file = og_user.files.filter(name=body["name"])

    if file.exists():
        return JsonResponse({
            "error": "There is already a file with that name."
        })

    file = File()
    file.name = body["name"]
    file.save()

    og_user.files.add(file)
    og_user.save()

    return JsonResponse({
        "user": og_user.obj()
    })


def save(request, file_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You need to be logged in to create a new file."
        })

    if request.method != "POST":
        return JsonResponse({
            "error": "This method is not allowed"
        })

    body = json.loads(request.body)

    if not body["content"]:
        return JsonResponse({
            "error": "Couldn't receive the content"
        })

    og_user = User.objects.get(username=request.user.username)

    file = og_user.files.filter(id=file_id)

    if not file.exists():
        return JsonResponse({
            "error": "This file either doesn't exist or you are not authorise to save it."
        })

    file = file.get(id=file_id)
    file.content = body["content"]
    file.modified = datetime.now(timezone.utc)
    file.save()

    return JsonResponse({
        "user": og_user.obj()
    })


def rename(request, file_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You need to be logged in to create a new file."
        })

    if request.method != "POST":
        return JsonResponse({
            "error": "This method is not allowed"
        })

    body = json.loads(request.body)

    if not body["name"] or len(body["name"]) < 3:
        return JsonResponse({
            "error": "You need to enter a name, minumum 3 characters"
        })

    og_user = User.objects.get(username=request.user.username)

    file = og_user.files.filter(name=body["name"])

    if file.exists():
        return JsonResponse({
            "error": "There is already a file with that name."
        })

    file = og_user.files.filter(id=file_id)

    if not file.exists():
        return JsonResponse({
            "error": "This file either doesn't exist or you are not authorise to save it."
        })

    file = file.get(id=file_id)
    file.name = body["name"]
    file.modified = datetime.now(timezone.utc)
    file.save()

    return JsonResponse({
        "user": og_user.obj()
    })


def delete(request, file_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You need to be logged in to create a new file."
        })

    if request.method != "POST":
        return JsonResponse({
            "error": "This method is not allowed"
        })

    og_user = User.objects.get(username=request.user.username)
    file = File.objects.filter(id=file_id)

    if not file.exists():
        JsonResponse({
            "error": "This file doesn't exists or you are not the rightful owner."
        })

    og_user.files.get(id=file_id).delete()
    og_user.save()

    return JsonResponse({
        "user": og_user.obj()
    })


def user(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "You need to be logged in to create a new file."
        })

    og_user = User.objects.get(username=request.user.username)

    return JsonResponse({
        "user": og_user.obj()
    })
