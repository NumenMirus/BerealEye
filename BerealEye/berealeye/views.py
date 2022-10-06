import pprint
from django.shortcuts import render, redirect
import berealeye.BFWrapper as bfw
from berealeye.BeFake.BeFake import BeFake
import berealeye.models as models


def index(request):
    
    user = BeFake()
    token = models.Tokens.objects.first()
    if not token:
        bfw.send_otp(user, '+393342594893')
        bfw.verify_otp(user, input('OTP: '))
        token = models.Tokens.objects.first().token
    
    token = models.Tokens.objects.first().token
    print("\n\n"+token, end="\n\n")

    me = bfw.me(user, token)
    

    feed = (bfw.get_feed_links(user, 'friends',token))
    feed_dicts= []
    for post in feed:
        feed_dicts.append(post.__dict__)

    #pprint.pprint(feed_dicts)
    context = {'feed_dicts': feed_dicts, 'me': me}
    return render(request, 'berealeye/index.html', context)

def refresh_token(request):
    user = BeFake()
    token = models.Tokens.objects.first()
    new_token = bfw.refresh(user, token.token)
    token.token = new_token
    token.save()
    return redirect('/')

def logout(request):
    token = models.Tokens.objects.first()
    token.delete()