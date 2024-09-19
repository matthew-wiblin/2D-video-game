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


# GET request for highscore with query parameter of username
def get_highscore(request):
    pass


# POST request for a new highscore
@csrf_exempt
def check_and_update_high_score(request):
    body_content = request.body.decode('utf-8')
    parts = body_content.split("=")
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

