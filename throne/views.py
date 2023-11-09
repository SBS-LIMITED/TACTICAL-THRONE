from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account, H_key
from os import urandom
import datetime
import blowfish
import secrets
import string

# Create your views here.
def index(request):
    return render(request, 'throne/index.html')

def login(request):
    global date, users, name, user 

    if request.method == 'POST':
        email = request.POST.get('e_mail')
        phone = request.POST.get('phone_no')
        password = request.POST.get('password')

        if Account.objects.filter(email=email).exists():
            user = Account.objects.filter(email=email)
            p_no = '0'+str(user[0].phone_no)

            data = H_key.objects.filter(user= email)
            enc_pass = data[0].password
            res = data[0].h_key
            iv = data[0].iv
           
            c_key = blowfish.Cipher(bytes(res.encode()))
            data_encrypted = b"".join(c_key.encrypt_cfb(bytes(password.encode()), iv))
            data_hex= data_encrypted.hex()


            if p_no == str(phone) and enc_pass == data_hex:
                print('[+] >> login successful: {}'.format(email))
                
                #metadata
                date = datetime.datetime.now()
                users = Account.objects.all()
                name = user[0].first_name

                context = {
                    'users': users,
                    'name': name,
                    'date': date
                }


                return render(request,'throne/userboard.html', context=context)
            else:
                messages.error(request, "login error, please check your credentials.")
                return redirect('login')
        else:
            messages.error(request, "login error, please check your credentials.")
            return redirect('login')
    else:
        return render(request, 'throne/login.html')


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('f_name')
        lname = request.POST.get('l_name')
        email = request.POST.get('e_mail')
        phone = request.POST.get('phone_no')
        password = request.POST.get('password')

        user = Account(first_name=fname, last_name=lname, email=email, phone_no=phone)
        user.save()

        #enc..
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(8))
        c_key = blowfish.Cipher(bytes(res.encode()))
        

        iv = urandom(8) # initialization vector
        print(type(iv))
        print(iv)
        data_encrypted = b"".join(c_key.encrypt_cfb(bytes(password.encode()), iv))
        data_hex= data_encrypted.hex()

        user = Account.objects.get(email=email)
        key = H_key(user= user, h_key=res, iv=iv, password= data_hex)
        key.save()


        #data_decrypted = b"".join(c_key.decrypt_cfb(bytes.fromhex(h), iv))
        
        print('[+] >> Account Created for {}'.format(fname))
        print(c_key)
        print(type(c_key))

        messages.success(request, "Account created successfully, please login.")
        return redirect('login')
    else:
        return render(request, 'throne/signup.html')

def about(request):
    return render(request, 'throne/about.html')

def userboard(request):
    context = {
        'users': users,
        'name': name,
        'date': date
    }
    return render(request, 'throne/userboard.html', context=context)

def feedback(request):
    return render(request, 'throne/feedback.html')

def settings(request):
    firstName = user[0].first_name
    lastName = user[0].last_name
    email = user[0].email
    phone = user[0].phone_no
    

    context = {
        'fName': firstName,
        'lName': lastName,
        'email': email,
        'phone': phone
    }

    return render(request, 'throne/settings.html', context=context)

def update(request, email):
    if request.method == 'POST':
        member = Account.objects.get(email=email)
        fname = request.POST.get('f_name')
        lname = request.POST.get('l_name')
        phone = request.POST.get('p_no')
        password = request.POST.get('password')

        member.first_name = fname
        member.last_name = lname
        member.phone_no = phone
        member.save()

        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(8))
        c_key = blowfish.Cipher(bytes(res.encode()))
        

        iv = urandom(8) # initialization vector
        print(type(iv))
        print(iv)
        data_encrypted = b"".join(c_key.encrypt_cfb(bytes(password.encode()), iv))
        data_hex= data_encrypted.hex()

        User = H_key.objects.get(user_id=email)
        User.h_key = res
        User.iv = iv
        User.password = data_hex
        User.save()
       

        messages.success(request, "Account Updated successfully, please login.")
        return redirect('login')
    else:
        pass

def invite(request):
    if request.method == 'POST':
        # opponent = Account.objects.filter(email=email)
        # fname = opponent[0].first_name
        # lname = opponent[0].last_name
        # phone = opponent[0].phone_no

        # context = {
        #     'fname' : fname,
        #     'lname' : lname,
        #     'phone' : phone,
        # }
        return render(request, 'throne/invite.html')

def gamecode(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        #code to send invite here
        #//

        return redirect('http://127.0.0.1:3037/white?code={}'.format(code))