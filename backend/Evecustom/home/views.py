from django import template
from django.shortcuts import get_object_or_404, redirect, render
from httpcore import request
from .utils import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
import random
from django.http import HttpResponse, JsonResponse
from home.models import HostProfile , ParticipantProfile
from host.models import Event
from participant.models import createteam as CreateTeam, jointeam as JoinTeam
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

def hostsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        organization = request.POST.get('organisation')
        password = request.POST.get('password')

        if HostProfile.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        if HostProfile.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please choose a different email.")
        
        session_otp = str(random.randint(100000, 999999))
        request.session['otp'] = session_otp
        signup_data = {
            'role': 'Host',
            'username': username,
            'email': email,
            'phone': phone,
            'organization': organization,
            'password': password
        }
        request.session['signup_data'] = signup_data

        # otp to mail
        send_mail_maltialt(email, session_otp)

        return render(request, 'otp.html')
    return render(request, 'hostsignup.html')

def participantsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        college = request.POST.get('college')
        year = request.POST.get('year')

        if ParticipantProfile.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        if ParticipantProfile.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please choose a different email.")
        
        session_otp = str(random.randint(100000, 999999))
        request.session['otp'] = session_otp
        signup_data = {
            'role': 'Participate',
            'username': username,
            'email': email,
            'phone': phone,
            'college': college,
            'year': year,
            'password': password
        }
        request.session['signup_data'] = signup_data

        send_mail_maltialt(email, session_otp)

        return render(request, 'otp.html')
    return render(request, 'participantsignup.html')

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
        if role == 'Participate':
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

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role=request.POST.get('role')

        if role == 'Host':
            if HostProfile.objects.filter(email=email).exists():
                Host = HostProfile.objects.get(email=email)
                data={'Host':Host}
                if check_password(password, Host.password):
                    request.session['host_id'] = Host.id
                    return redirect('hostdash')
                else:
                    return HttpResponse("Invalid host credentials.")
            else:
                return HttpResponse("Host with this email does not exist.")
            
        elif role == 'Participant':
            if ParticipantProfile.objects.filter(email=email).exists():
                User = ParticipantProfile.objects.get(email=email)
                data={'User':User}
                if check_password(password, User.password):
                    request.session['user_id'] = User.id
                    return redirect('partdas')
                else:
                    return HttpResponse("Invalid participant credentials.")
            else:
                return HttpResponse("Participant with this email does not exist.")
    return render(request, 'login.html') 

def hostdash(request):
    if 'host_id' not in request.session:
        return redirect('login')
    host_id = request.session['host_id']
    host_profile = HostProfile.objects.get(id=host_id)
    events = Event.objects.filter(host=host_profile)
    data = {
        'host': host_profile,
        'events': events
    }
    return render(request, 'hostdash.html', data)

def signupportal(request):
    return render(request, 'signupportal.html')

def partdas(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    User = ParticipantProfile.objects.get(id=request.session['user_id'])
    events=Event.objects.all()
    data={'events':events, 'User':User}
    return render(request, 'partdas.html',data)

def otp_verification_team(request):
    if 'team_data' not in request.session or 'otp' not in request.session:
        return render(request, 'createteam.html')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        role=request.session['team_data']['role']
        if role == 'CreateTeam':
            if entered_otp == session_otp:
                team_data = request.session.get('team_data')
                event_name = team_data['event']
                event = Event.objects.get(name=event_name)
                username = ParticipantProfile.objects.get(username=team_data['username'])
                team_code = team_data['team_code']
                team_name = team_data['team_name']
                team_leader = team_data['team_leader']
                email = team_data['email']
                github_account = team_data['github_account']
                team_members = team_data['team_members']
                tnc = team_data['tnc']

                createteam_obj = CreateTeam(
                    event=event,
                    username=username,
                    team_code=team_code,
                    team_name=team_name,
                    team_leader=team_leader,
                    email=email,
                    gitaccount=github_account,
                    team_members=team_members,
                    tnc=tnc
                )
                createteam_obj.save()
                send_create_team_mail(email, team_name, team_code, event_name)
                del request.session['team_data']
                del request.session['otp']
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
        if role == 'JoinTeam':
            if entered_otp == session_otp:
                team_data = request.session.get('team_data')
                event_name = team_data['event']
                event = Event.objects.get(name=event_name)
                username = ParticipantProfile.objects.get(username=team_data['username'])
                team_code = team_data['team_code']
                team_name = team_data['team_name']
                name = team_data['name']
                email = team_data['email']
                github_account = team_data['github_account']
                tnc = team_data['tnc']

                print(event,username)
                jointeam_obj = JoinTeam(
                    event=event,
                    username=username,
                    team_code=team_code,
                    team_name=team_name,
                    name=name,
                    email=email,
                    gitaccount=github_account,
                    tnc=tnc
                )
                jointeam_obj.save()
                send_join_team_mail(email, team_name, team_code, event_name)
                del request.session['team_data']
                del request.session['otp']
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
    return render(request, 'teamotp.html')



def generate_team_code():
    length = 8
    while True:
        team_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
        if not CreateTeam.objects.filter(team_code=team_code).exists():
            return team_code

def createteam(request,id):
    if 'user_id' not in request.session:
        return redirect('login')
    event=get_object_or_404(Event, id=id)
    if request.method == 'POST':
        user_id = request.session['user_id']
        participant_profile = ParticipantProfile.objects.get(id=user_id)
        team_name = request.POST.get('team_name')
        team_leader_name = request.POST.get('team_leader_name')
        email = request.POST.get('email')
        github_account = request.POST.get('github_account')
        team_members = request.POST.get('team_members')
        tnc = request.POST.get('tnc') == 'on'
        if CreateTeam.objects.filter(team_name=team_name, event=event ).exists():
            return HttpResponse("Team name already exists for this event. Please choose a different team name.")
        team_code = generate_team_code()
        print(event.name,participant_profile.username)

        session_otp = str(random.randint(100000, 999999))
        request.session['otp'] = session_otp

        team_data = {
            'role': 'CreateTeam',
            'event': event.name,
            'username': participant_profile.username,
            'team_code': team_code,
            'team_name': team_name,
            'team_leader': team_leader_name,
            'email': email,
            'github_account': github_account,
            'team_members': team_members,
            'tnc': tnc
        }
        request.session['team_data'] = team_data

        send_mail_maltialt(email, session_otp)

        return render(request, 'teamotp.html')

    return render(request, 'createteam.html')

def jointeam(request,id):
    if 'user_id' not in request.session:
        return redirect('login')
    event=get_object_or_404(Event, id=id)
    if request.method == 'POST':
        user_id = request.session['user_id']
        participant_profile = ParticipantProfile.objects.get(id=user_id)
        team_code = request.POST.get('team_code')
        name = request.POST.get('user_name')
        email = request.POST.get('email')
        github_account = request.POST.get('github_account')
        tnc = request.POST.get('tnc') == 'on'

        if not CreateTeam.objects.filter(team_code=team_code, event=event ).exists():
            return HttpResponse("Invalid team code for the selected event.")
        

        session_otp = str(random.randint(100000, 999999))
        request.session['otp'] = session_otp
        print(event.name,participant_profile.username)

        team_data = {
            'role': 'JoinTeam',
            'event': event.name,
            'username': participant_profile.username,
            'team_code': team_code,
            'team_name': CreateTeam.objects.get(team_code=team_code).team_name,
            'name': name,
            'email': email,
            'github_account': github_account,
            'tnc': tnc
        }
        request.session['team_data'] = team_data

        send_mail_maltialt(email, session_otp)

        return render(request, 'teamotp.html')
    return render(request, 'jointeam.html')

def eventwise(request,id):
    if 'user_id' not in request.session:
        return redirect('login')
    event=Event.objects.get(id=id)
    User=ParticipantProfile.objects.get(id=request.session['user_id'])
    data={'event':event, 'User':User}
    return render(request, 'eventwise.html', data)