from django import template
from django.shortcuts import redirect, render
from .utils import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
import random
from django.http import HttpResponse, JsonResponse
from home.models import HostProfile , ParticipantProfile
from host.models import Event
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
  

def generate_id_card(idc):
    # l = [Username,Event_name,Organization ]
    output_dir = f"files_data/user/{idc[0]}"
    save_path = os.path.join(output_dir,f"{idc[1]}_id.png")
    formate_path = "static/images/idcard.png"


    template = Image.open(formate_path).convert("RGBA")

    draw = ImageDraw.Draw(template)
    font_user = ImageFont.truetype("arialbd.ttf", 80)
    font_event = ImageFont.truetype("arial.ttf", 60)
    font_org = ImageFont.truetype("arial.ttf", 50)

    TEXT_X = 260

    draw.text((130, 500), f"{idc[0]}", fill="white", font=font_user)
    draw.text((100, 730), f"{idc[1]}", fill="white", font=font_event)
    draw.text((105, 820), f"{idc[2]}", fill="white", font=font_org)

    qr_data = f"Organization: {idc[0]}\nEvent: {idc[1]}\nUsername: {idc[2]}"
    qr = qrcode.make(qr_data)
    qr = qr.resize((150, 150))

    QR_X = 460
    QR_Y = 750

    template.paste(qr, (QR_X, QR_Y))
    template.save(save_path)
    print(f"ID card saved at: {save_path}")


def generate_certificate(cer):
    # l = ["Username","Event_name","hostname","Organization"]

    output_dir = f"files_data/user/{cer[0]}"
    save_path = os.path.join(output_dir,f"{cer[1]}_certificate.png")
    formate_path = "static/images/certificate.png"

    template = Image.open(formate_path).convert("RGBA")
    draw = ImageDraw.Draw(template)

    font_org = ImageFont.truetype("arialbd.ttf", 100)
    font_event = ImageFont.truetype("arial.ttf", 38)
    font_user = ImageFont.truetype("arial.ttf", 60)
    font_host = ImageFont.truetype("arial.ttf", 40)

    draw.text((650, 480), f"{cer[0]}", fill="black", font=font_org)
    draw.text((1210, 620), f"{cer[1]}", fill="black", font=font_event)
    draw.text((580, 876), f"{cer[2]}", fill="black", font=font_user)
    draw.text((600, 978), f"{cer[3]}", fill="black", font=font_host)

    template.save(save_path)
    print(f"Certificate saved at: {save_path}")
    
# Create your views here.
def home(request):
    return render(request, 'index.html')

def otp(request):
    if 'signup_data' not in request.session or 'otp' not in request.session:
        return render(request, 'index.html')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        role=request.session['signup_data']['role']
        if role == 'Host':
            if entered_otp == session_otp:
                signup_data = request.session.get('signup_data')
                username = signup_data['username']
                email = signup_data['email']
                phone = signup_data['phone']
                organization = signup_data['organization']
                hashed_password = make_password(signup_data['password'])

                # save to database
                host_profile = HostProfile(username=username, email=email, phone=phone, organization=organization, password=hashed_password)
                host_profile.save()

                # create directory for host
                host_directory = os.path.join(settings.BASE_DIR, 'files_data', 'host', str(host_profile.username))
                os.makedirs(host_directory, exist_ok=True)

                del request.session['signup_data']
                del request.session['otp']
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
        if role == 'Participant':
            if entered_otp == session_otp:
                signup_data = request.session.get('signup_data')
                username = signup_data['username']
                email = signup_data['email']
                phone = signup_data['phone']
                college = signup_data['college']
                year = signup_data['year']
                hashed_password = make_password(signup_data['password'])

                user_profile = ParticipantProfile(username=username, email=email, phone=phone, college=college, year=year, password=hashed_password)
                user_profile.save()

                user_directory = os.path.join(settings.BASE_DIR, 'files_data', 'user', str(user_profile.username))
                os.makedirs(user_directory, exist_ok=True)

                del request.session['signup_data']
                del request.session['otp']
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
    return render(request, 'otp.html')

