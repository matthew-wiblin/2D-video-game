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
# Much of the username and password checking is done customer side as well
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
                print("User exists")
                return HttpResponse("User exists", status=409)
            except UserData.DoesNotExist:
                user_data = UserData(username=username, password=password)
                user_data.save()
                print("User created")
                return HttpResponse("User created", status=201)
        else:
            print("Failed")
            return HttpResponse("Failed", status=400)
    print("Method failed")
    return HttpResponse("Method failed", status=405)


# GET request for user data with query parameter of username and password (log in)
def get_user_data(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    if not username or not password:
        print("Username or password not provided")
        return HttpResponse("Username or password  not provided", status=400)
    
    try:
        user_data = UserData.objects.get(username=username)
        if user_data.password == password:
            response = f"{user_data.username}--{user_data.highscore}--{user_data.most_aliens_killed_in_one_game}"
            print("User login success")
            return HttpResponse(response, status=200)
        else:
            print("Incorrect password")
            return HttpResponse("Incorrect password", status=403)
    except UserData.DoesNotExist:
        print("User not found")
        return HttpResponse("User not found", status=404)


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
    return HttpResponse("method failed", status=405)

