from datetime import datetime
import datetime
from logging import exception
from django.shortcuts import redirect, render
import random
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.core import serializers
import datetime
from django.core import serializers
from django.http import Http404, HttpResponse
import os
from django.http import HttpResponse

# session call options::

def register(request):
    if request.POST:
        try:
            name = request.POST["Name"]
            email = request.POST["Email"]
            phone = request.POST["Phone"]
            employe_id = request.POST["Employe_id"]
            role = request.POST["role"]
            data = ["sdf78",'skf858','ghd65','ghf32','tgf20']
            password = random.choice(data)+email[3:7]
            u = User.objects.create(email = email,password = password,role = role,name = name,phone=phone,Employe_id=employe_id)
            if role=="HR":
                uid = HR.objects.create(password = password,role = role,name = name,phone=phone,Employe_id=employe_id,email = email)
                if uid:
                    send_mail("confirmation mail","your system generated password is "+password,"17janpython@gmail.com",[email])
                    s_msg = "sucessfully account created"
                    context = {
                        "s_msg" : s_msg
                    }
                    # del request.session['email']
                    return render(request,"my_app/register.html",context)
            elif role=="Employe":
                nid = Employe.objects.create(password = password,role = role,name = name,phone=phone,Employe_id=employe_id,email = email)
                if nid:
                    send_mail("confirmation mail","your system generated password is "+password,"17janpython@gmail.com",[email])
                    s_msg = "sucessfully account created"
                    context = {
                        "s_msg" : s_msg
                    }
                    # del request.session['email']  
                    return render(request,"my_app/register.html",context)
        except Exception as e:
            print('Exception called')
            print(e)
            s_msg = "sucessfully account created"
            return render(request,"my_app/register.html",{"s_msg":s_msg})
        except:
            e_msg = "something went wrong!"
            context = {
                "x_msg" : e_msg
            }
            return render(request,"my_app/register.html",context)
    else:
        print("only page loaded")
        return render(request,"my_app/register.html") 
    
# def button(request):
#     email = request.POST["email"]
#     password = request.POST["password"]
#     # role = request.POST["role"]
#     emp=Employe.objects.filter(email = email,password = password)
#     return JsonResponse({"emp":emp}) 
        
@ csrf_exempt
def login(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        if uid.role == 'HR':
            uid = HR.objects.get(email = request.session['email'])
            project_counter = Project.objects.count()
            client_counter = client_client.objects.count()
            employee_counter = Employe.objects.count()
            return render(request,'my_app/dashbord/index.html',{'uid':uid,'project_counter':project_counter,'client_counter':client_counter,'employee_counter':employee_counter})
        
        if uid.role == 'Employe':
            nid = Employe.objects.get(email = request.session["email"])
            project_counter = Project.objects.count()
            client_counter = client_client.objects.count()
            employee_counter = Employe.objects.count()
            context = {
                'project_counter' : project_counter,
                'client_counter' : client_counter,
                'employee_counter' : employee_counter,
                "nid" : nid,
            }
            return render(request,'my_app/dashbord/index.html',context)
        else:   
            e_msg = "something wen's wrong"
            return render(request,"my_app/login.html",{"e_msg":e_msg}) 
    elif request.POST:
            role = request.POST["role"]
            if role == 'HR':
                email = request.POST["email"]
                password = request.POST["password"]
                try:
                    uid = User.objects.get(email=email,password=password)
                    if uid.password == password:
                        if uid.is_verify == False:
                            return render(request,"my_app/change-password.html",{"email":email,"role":role})
                        else:
                            project_counter = Project.objects.count()
                            client_counter = client_client.objects.count()
                            employee_counter = Employe.objects.count()
                            request.session['email'] = uid.email
                            context = {
                                "uid" : uid,
                                'email':email,
                                "role" : role,
                                'project_counter':project_counter,
                                'client_counter':client_counter,
                                'employee_counter' : employee_counter,
                            }
                            return render(request,"my_app/dashbord/index.html",context) 
                    else:
                        e_msg = 'kuch to gadbad he daya!!!'
                        return render(request,'my_app/login.html',{'e_msg':e_msg})
                except:
                    e_msg = "Invalid email or password!!"
                    context = {
                        "e_msg" : e_msg
                    }    
                    return render(request,"my_app/login.html",context)    
            elif role == 'Employe':            
                email = request.POST["email"]
                password = request.POST["password"]
                try:
                    nid = Employe.objects.get(email=email,password=password,role=role)
                    if nid.password == password:
                        if nid.is_verify == False:
                            return render(request,"my_app/change-password.html",{"email":email,"role":role})
                        else:
                            request.session['email'] = nid.email
                            project_counter = Project.objects.count()
                            client_counter = client_client.objects.count()
                            employee_counter = Employe.objects.count()
                            context = {
                                "nid" : nid,
                                'email':email,
                                'project_counter':project_counter,
                                'client_counter':client_counter,
                                'employee_counter' : employee_counter,
                            }
                            return render(request,"my_app/dashbord/index.html",context) 
                except:
                    e_msg = "Invalid email or password!!"
                    context = {
                        "e_msg" : e_msg
                    }    
                    return render(request,"my_app/login.html",context) 
                            
            else:
                e_msg = 'kuch to gadbad he daya!!!'
                return render(request,'my_app/login.html',{'e_msg':e_msg})            
        
    else:
        return render(request,'my_app/login.html')       

def c_password(request):
    if request.POST:
        role = request.POST["role"]
        email = request.POST["email"]
        oldpassword = request.POST["oldpassword"]
        newpassword = request.POST["newpassword"]
        confirmpassword = request.POST["confirmpassword"]
        uid = User.objects.get(email= email,password = oldpassword)
        if newpassword == confirmpassword:
            if uid.password == oldpassword:
                uid.password = newpassword
                uid.is_verify = True
                uid.save()
                if role == "HR":
                    uid = HR.objects.get(email= email,password = oldpassword)
                    if uid.password == oldpassword:
                        uid.password = newpassword
                        uid.is_verify = True
                        uid.save()
                        s_msg = 'Change password succesfully created!!!'
                        return render(request,"my_app/login.html",{"s_msg":s_msg})
            
                elif role == "Employe":
                    if Employe.objects.get(email=email,password = oldpassword):
                        nid = Employe.objects.get(email=email,password = oldpassword)
                        if nid.password == oldpassword:
                            nid.password = newpassword
                            nid.is_verify = True
                            nid.save()
                            s_msg = 'Change password succesfully created!!!'
                            return render(request,"my_app/login.html",{"s_msg":s_msg})
                        
                else:
                    e_msg = "Invalid!! old password does not match!!"
                    return render(request,"my_app/change-password.html",{"email":email})
                        
        else:
            e_msg = "Invalid!! old password does not match!!"
            return render(request,"my_app/change-password.html",{"email":email,"e_msg":e_msg})
    else:
        e_msg = "Invalid!! old password does not match!!"
        return render(request,"my_app/change-password.html",{"e_msg":e_msg})     

def logout(request):
    if 'email' in request.session:
        del request.session["email"]
        return render(request,"my_app/login.html")  

# gad-bad he daya!!!!!!!!!!!!!!!!!!!!!!
def projects(request):
    if request.POST:
        pid = Project.objects.create(Project_name = request.POST['Project_name'],
                                    start_date= request.POST["Start_date"],
                                    end_date = request.POST['End_date'],
                                    Priority = request.POST["class"],
                                    Project_leader = request.POST["project_leader"],
                                    add_team1 = request.POST["team1"],
                                    add_team2 = request.POST["team2"],
                                    add_team3 = request.POST["team3"],
                                    add_team4 = request.POST["team4"],
                                    describe = request.POST["Description"],
                                    logo = request.POST["file"],
                                    )
        if "logo" in request.FILES:
            pid.logo = request.FILES['file']         
            pid.save()
        pid.save()  
        all_data = Project.objects.all()
        uid = HR.objects.get(email = request.session["email"])
        context = {"all_data":all_data,"uid":uid}  
        return render(request,"my_app/dashbord/projects.html",context)
    else:
        all_data = Project.objects.all()
        nid = User.objects.get(email = request.session["email"])
        if nid.role == "HR":
            uid = HR.objects.get(email = request.session["email"])
            context = {"all_data":all_data,"uid":uid} 
            return render(request,"my_app/dashbord/projects.html",context)
        elif nid.role == "Employe":
            nid = Employe.objects.get(email = request.session["email"])
            context = {"all_data":all_data,"nid":nid} 
            return render(request,"my_app/dashbord/projects.html",context)

def search(request):
    if request.POST:
        all__data = Project.objects.filter(Project_name=request.POST["Project__name"])
        uid = HR.objects.get(email = request.session["email"])
        context = {"all__data":all__data,"uid":uid}
        return render(request,"my_app/dashbord/projects.html",context)

    else:
        return render(request,"my_app/dashbord/projects.html")
# password ma error he!!!
def all_list(request):
    if request.POST:
        aid = Employe.objects.create(name=request.POST["First_name"],
                                    last_name=request.POST["Last_name"],
                                    email=request.POST["Email"],
                                    phone=request.POST["phone"],
                                    date=request.POST["date"],
                                    Employe_id=request.POST["Employee_id"],
                                    password = request.POST["Password"],
                                    designation=request.POST["Designation"],
                                    department=request.POST["Department"],
        )
        data = ["sdf78",'skf858','ghd65','ghf32','tgf20']
        #password = random.choice(data)+email[3:7]
        #send_mail("confirmation mail","your system generated password is "+password,"17janpython@gmail.com",[email])
        all_list = Employe.objects.all()
        uid = HR.objects.get(email = request.session["email"])
        context = {
            "all_list":all_list,
            "uid" : uid
        }
       
        return render(request,"my_app/dashbord/all_list.html",context)    
    else:
        uid = HR.objects.get(email = request.session['email'])
        
        all_list = Employe.objects.all()
        return render(request,"my_app/dashbord/all_list.html",{"uid":uid,"all_list":all_list})

def delete(request,pk):
    try:
        va = Employe.objects.get(pk=pk)
        va.delete()
        return redirect('all_list')
    except exception as e:
        print(e)
        return render(request,"my_app/dashbord/all_list.html")   

def update(request,pk):
    try:
        na = Project.objects.get(pk=pk)
        na.delete()
        return redirect('projects')
    except exception as e:
        print(e)
        return render(request,"my_app/dashbord/projects.html")
@csrf_exempt
def search_employe(request):
    if request.POST:
        all_list = Employe.objects.filter(name = request.POST["Employe_name"])
        uid = HR.objects.get(email = request.session["email"])
        return render(request,"my_app/dashbord/all_list.html",{"all_list":all_list,"uid":uid})

def attendance_Hr(request):
    hrd = HR.objects.all()
    uid = HR.objects.get(email = request.session["email"])
    if uid.role == "HR":
        return render(request,"my_app/dashbord/attendance-Hr.html",{"hrd":hrd,"uid":uid})
    else:
        return render(request,"my_app/dashbord/attendance-Hr.html")
def puch_in(request):
    if request.POST:
        puch = HR.objects.get(email = request.session['email'])
        puch.date = datetime.date.today()
        puch.puch_in = datetime.datetime.now()
        puch.save()
        if puch.date == datetime.date.today():
            return redirect('attendance_Hr')
        else:
            today = datetime.date.today()
            hrd = HR.objects.filter(date = today) 
            uid = HR.objects.get(email = request.session["email"])
            return render(request,"my_app/dashbord/attendance-Hr.html",{"hrd":hrd,"uid":uid})

def puch_out(request):
    if request.POST:
        puch = HR.objects.get(email = request.session["email"])
        puch.puch_out = datetime.datetime.now()
        puch.date = datetime.date.today()
        puch.save()
        if puch.date == datetime.date.today():
            return redirect('attendance_Hr')
        else:
            today = datetime.date.today()
            hrd = HR.objects.filter(date = today) 
            uid = HR.objects.get(email = request.session["email"])
            return render(request,"my_app/dashbord/attendance-Hr.html",{"hrd":hrd,"uid":uid})

def salary(request):
    uid = HR.objects.get(email = request.session["email"])  
    staff = Employe.objects.all()
    if uid.role == "HR":
        return render(request,"my_app/dashbord/salary.html",{"staff":staff,"uid":uid})

@csrf_exempt
def initiate_payment(request):
    eid = Employe.objects.get(name = request.POST["name"])
    eid.salary = request.POST["amount"]
    eid.save()
    user = HR.objects.get(email=request.session["email"])
    try:
        amount = int(request.POST['amount'])
    except:
        return render(request, 'my_app/dashbord/salary.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
    )

    paytm_params = dict(params)
    
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    
    # paytm_params['CHECKSUMHASH'] = checksum
    cotext = {
        'CHECKSUMHASH' : checksum,
        'eid.name' : eid.name,
    }
    # print('----------------------------------------============> context',cotext)
    print('SENT: ', checksum)
    return render(request, 'my_app/dashbord/redirect.html',cotext)


def callback(request):
    if request.method == 'POST':   
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'my_app/dashbord/callback.html', context=received_data)
    return render(request, 'my_app/dashbord/callback.html', context=received_data)

def CB(request):
    return render(request, 'my_app/dashbord/callback.html')

def Performance(request):
    uid = User.objects.get(email = request.session["email"])
    if uid.role == "HR":
        randome = random.randint(0,100)
        uid = HR.objects.get(email = request.session["email"])
        return render(request,"my_app/dashbord/performance.html",{"uid":uid,"randome":randome})
    elif uid.role == "Employe":
        randome = random.randint(0,100)
        nid = Employe.objects.get(email = request.session["email"])
        return render(request,"my_app/dashbord/performance.html",{'nid':nid,"randome":randome})
    else:
        return render(request,"my_app/dashbord/performance.html")
        
def valid_name(request):
    username = request.POST["username"]
    emp=Employe.objects.filter(name=username)
    post_list = serializers.serialize('json',list(emp),fields=('name','last_name','email','date','Employe_id','salary','designation','department'))
    return HttpResponse(post_list)

def attendance_employe(request):
    hrd = Employe.objects.all()
    u_id = User.objects.get(email = request.session['email'])
    if u_id.role == "Employe":
        nid = Employe.objects.get(email = request.session["email"])
        context = {
            "hrd":hrd,
            "nid" : nid,
            "u_id":u_id,
        }
        return render(request,"my_app/dashbord/attendance-employe.html",context)    
    elif u_id.role == "HR":
        uid = HR.objects.get(email = request.session["email"])
        context = {
            "hrd":hrd,
            "uid" : uid,
            "u_id":u_id,
        }
        return render(request,"my_app/dashbord/attendance-employe.html",context)  
        

def contacts(request):
    if request.POST:
        uid = HR.objects.get(email = request.session["email"])
        client = client_client.objects.create(name = request.POST["name"],phone = request.POST["contact"])
        client = client_client.objects.all()
        return render(request,"my_app/dashbord/contacts.html",{"client":client,"uid":uid})
    else:
        uid = HR.objects.get(email = request.session["email"])
        client = client_client.objects.all()
        return render(request,"my_app/dashbord/contacts.html",{"client":client,"uid":uid})
    

def uid(request):
    uid = HR.objects.get(email = request.session["email"])
    nid = Employe.objects.all()
    return render(request,"my_app/dashbord/contacts.html",{"nid":nid,"uid":uid})
        
def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type= "application/logo")
            response['content-disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404    
            
def file_manager(request):
    if "email" in request.session:
        if request.POST:
            file.objects.create(files = request.FILES["files"])
            uid = User.objects.get(email = request.session["email"])
            if uid.role == "HR":
                F = file.objects.all()
                return render(request,"my_app/dashbord/file-manager.html",{"F":F,"uid":uid})
            else:
                nid = Employe.objects.get(email = request.session["email"])
                F = file.objects.all()
                return render(request,"my_app/dashbord/file-manager.html",{"F":F,"nid":nid})
        else:
            if "email" in request.session:
                F = file.objects.all()
                uid = User.objects.get(email = request.session["email"])
                return render(request,"my_app/dashbord/file-manager.html",{'F':F,'uid':uid})    

def re_search(request):
    name = request.POST["Employe_n"]
    email = request.POST["Employe_Email"]
    staff = Employe.objects.filter(name = name,email=email)
    uid = HR.objects.get(email = request.session["email"])
    return render(request,"my_app/dashbord/salary.html",{"staff":staff,"uid":uid})
def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        if uid.role == "HR":
            uid = HR.objects.all()
            return render(request,"my_app/dashbord/profile.html",{'uid':uid})
        elif uid.role == "Employe":
            nid = Employe.objects.all()
            return render(request,"my_app/dashbord/profile.html",{'nid':nid})


def change_password_profile(request):
    if request.POST:
        change_password = request.POST["Change_Password"]
        confirm_password = request.POST["Confirm_Password"]
        ui = User.objects.get(email = request.session['email'])
        if ui.role == "HR":
            if change_password == confirm_password:
                uid = HR.objects.get(email = request.session["email"])
                uid.password = change_password
                uid.save()
                del request.session['email']
                return redirect('login')
            else:
                e_msg = "something went's wrong!!" 
                context = {
                    "e_msg" : e_msg,
                }
                return redirect('profile',context)
        elif ui.role == "Employe":
            if change_password == confirm_password:
                nid = Employe.objects.get(email = request.session["email"])
                nid.password = change_password
                nid.save()
                del request.session['email']
                return redirect('login')
            else:
                e_msg = "something went's wrong!!" 
                context = {
                    "e_msg" : e_msg,
                }
                return redirect('profile',context)
      

      
                                                        

      






