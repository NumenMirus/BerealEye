import logging
import os
import pprint
from berealeye.BeFake.BeFake import BeFake
from berealeye.models import Tokens
import httpx

def send_otp(user, phone_number: str):
    user.send_otp(phone_number)

def verify_otp(user, otp: str) -> str:
    user.verify_otp(otp)
    t = user.save()
    token = Tokens(token=t)
    token.save()

def me(user, token: str) -> dict:
    user.load(token)
    user = user.get_user_info()
    return user.__dict__

def refresh(user, token: str):
    try:
        user.load(token)
    except:
        raise Exception("No token found, are you logged in?")
    user.refresh_tokens()
    print("New token: ", user.token)
    new_token = user.save()
    return new_token

def download_media(client: httpx.Client, item):
    return [
        client.get(item["photoURL"]).content,
        client.get(item["secondaryPhotoURL"]).content,
    ]

def download_feed(user, feed_id, token):
    try:
        user.load(token)
    except:
        raise Exception("No token found, are you logged in?")
    if feed_id == "friends":
        feed = user.get_friends_feed()

    elif feed_id == "discovery":
        feed = user.get_discovery_feed()

    os.makedirs(f"feeds/{feed_id}", exist_ok=True)
    for item in feed:
        os.makedirs(f"feeds/{feed_id}/{item.user.username}/{item.id}", exist_ok=True)

        # with open(
        #     f"feeds/{feed_id}/{item.user.username}/{item.id}/info.json",
        #     "w",
        # ) as f:
        #     f.write(json.dumps(item))

        with open(
            f"feeds/{feed_id}/{item.user.username}/{item.id}/primary.jpg",
            "wb",
        ) as f:
            f.write(item.primary_photo.download())
        with open(
            f"feeds/{feed_id}/{item.user.username}/{item.id}/secondary.jpg",
            "wb",
        ) as f:
            f.write(item.secondary_photo.download())
        for emoji in item.realmojis:
            os.makedirs(
                f"feeds/{feed_id}/{item.user.username}/{item.id}/reactions/{emoji.type}",
                exist_ok=True,
            )

            with open(
                f"feeds/{feed_id}/{item.user.username}/{item.id}/reactions/{emoji.type}/{emoji.username}.jpg",
                "wb",
            ) as f:
                f.write(emoji.photo.download())

def get_feed_links(user, feed_id, token):
    
    try:
        user.load(token)
    except:
        raise Exception("No token found, are you logged in?")
    if feed_id == "friends":
        feed = user.get_friends_feed()

    elif feed_id == "discovery":
        feed = user.get_discovery_feed()
    
    return feed

def get_user_from_phone_number(user, phone_number):
    return user.get_users_by_phone_number([phone_number])[0]

if __name__ == '__main__':
    user = BeFake()
    send_otp(user, '+393342594893')
    verify_otp(user, input('OTP: '))
    token = Tokens.objects.first()['token']
    print(token)