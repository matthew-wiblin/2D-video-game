from django.shortcuts import render, HttpResponse
from .models import UserData
from django.views.decorators.csrf import csrf_exempt

# No JSON functionality here as not implemented in unreal yet.
# POST and GET methods work with URL-encoded data and HttpResponses

def home(request):
    return HttpResponse("Hello django")


# GET request to retrieve leaderboard - top 5
def retrieve_leaderboard(request):
    top_scores = UserData.objects.order_by('-highscore')[:5]
    response = "--".join([f"{user.username} = {user.highscore}" for user in top_scores])
    return HttpResponse(response)


# POST request to create a user
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        body_content = request.body.decode('utf-8')
        parts = body_content.split("--")
        if len(parts) == 2:
            username = parts[0]
            password = parts[1]
            try:
                user_present = UserData.objects.get(username=username)
                print("user exists")
                return HttpResponse("user exists", status=409)
            except UserData.DoesNotExist:
                user_data = UserData(username=username, password=password)
                user_data.save()
                print("user created")
                return HttpResponse("user created", status=201)
        else:
            print("failed")
            return HttpResponse("failed", status=400)
    return HttpResponse("method failed", status=405)


# GET request for user data with query parameter of username (log in)
def get_user_data(request):
    username = request.GET.get(username)
    user_data = UserData.objects.get(username=username)
    response = f"{user_data.username}--{user_data.highscore}--{user_data.most_aliens_killed_in_one_game}"
    return HttpResponse(response) 


# POST request for a new highscore
@csrf_exempt
def sendscore(request):
    if request.method == "POST":
        body_content = request.body.decode('utf-8')
        parts = body_content.split("--")
        username = parts[parts.index("username") + 1]
        recentscore = float(parts[parts.index("recentscore") + 1])

        try:
            user_data = UserData.objects.get(username=username)
            if recentscore > user_data.highscore:
                user_data.highscore = recentscore
                user_data.save()
                return HttpResponse("New highscore saved")
            else:
                return HttpResponse("Nothing changed")
        except UserData.DoesNotExist:
            user_data = UserData(username=username, highscore=recentscore)
            user_data.save()
            return HttpResponse("New User and score saved")
        return HttpResponse("error: nothing passed")

