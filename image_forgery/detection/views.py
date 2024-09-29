from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import smtplib
from detection.models import UserRegistration,UserLogin,UserImage,ImageDetails,Feedback
import os
from django.core.files.storage import FileSystemStorage
from image_forgery.settings import BASE_DIR
import cv2
import numpy as np

# Create your views here.
def index(request):
    return render(request,'index.html')

def insertreg(request):
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        s5 = request.POST.get('t5', '')
        s6 = request.POST.get('t6', '')
        if s5==s6:
            UserRegistration.objects.create(name=s1, address=s2, phone=s3, email=s4,   password=s5)
            UserLogin.objects.create(username=s4, password=s5, utype="user")
        return render(request, 'registration.html', context={'msg': 'registration successfull'})
    return render(request, 'registration.html')

def logcheck(request):
    if request.method == "POST":
        uname = request.POST.get('t1', '')
        request.session['username'] = uname
        pwd = request.POST.get('t2', '')
        checklogin = UserLogin.objects.filter(username=uname).values()
        for a in checklogin:
            utype = a['utype']
            upass = a['password']
            if (upass == pwd):
                if (utype == "admin"):
                    return render(request, 'admin_home.html')
                if (utype == "user"):
                    return render(request, 'user_home.html')
                else:
                    return render(request, 'login.html', context={'msg': 'check username or password'})
            return render(request, "login.html", context={'msg': 'check username or password'})
        return render(request, "login.html", context={'msg': 'check username or password'})
    return render(request, "login.html")

def showuser(request):
    userdict = UserRegistration.objects.all()
    return render(request, 'viewregistration.html', {'userdict': userdict})

def deluser(request,pk):
    rid = UserRegistration.objects.get(id=pk)
    rid.delete()
    userdict = UserRegistration.objects.all()
    return render(request, 'viewregistration.html', {'userdict': userdict})

def userhome(request):
    return render(request,'user_home.html')

def adminhome(request):
    return render(request,'admin_home.html')


def send_email(request):
    content="Mail bantane?"
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('shwethasirsi16@gmail.com','ezwbwyguthzsklog')
    mail.sendmail('shwethasirsi16@gmail.com','bhavanabhat327@gmail.com',content)
    mail.close()
    return render(request,'send_mail.html')

def image_upload(request):
    if request.method=="POST" and request.FILES['myfile']:
            imgtype = request.POST.get('t1')
            imgname=request.POST.get('t2')
            myfile=request.FILES['myfile']
            details=request.POST.get('t3')
            date=request.POST.get('t4')
            by = request.POST.get('t5')

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            pat = os.path.join(BASE_DIR, '/media/' + filename)
            ImageDetails.objects.create(image_type=imgtype,image_name=imgname,image_location=myfile,details=details,created_date=date,created_by=by)
    return render(request,"imageupload.html")

def fileupload(request):
    if request.method=="POST" and request.FILES['myfile']:
            name = request.POST.get('t1')
            myfile=request.FILES['myfile']
            date=request.POST.get('t2')
            details=request.POST.get('t4')
            type=request.POST.get('t3')

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            pat = os.path.join(BASE_DIR, '/media/' + filename)
            UserImage.objects.create(user_name=name,image_type=type,date=date,details=details,imglocation=myfile)
    return render(request,"fileupload.html")

def showimage(request):
    userdict = UserImage.objects.all()
    return render(request, 'user_img_list.html', {'userdict': userdict})

def viewimage(request):
    userdict = ImageDetails.objects.all()
    return render(request, 'original_img_list.html', {'userdict': userdict})


def selectimage(request,pk):
    oid=ImageDetails.objects.filter(id=pk).all()
    userdict = UserImage.objects.all()
    return render(request, 'user_img_list.html', {'userdict': userdict,'oid':oid})

def delshowimg(request,pk):
    rid = UserImage.objects.get(id=pk)
    rid.delete()
    userdict = UserImage.objects.all()
    return render(request, 'user_img_list.html', {'userdict': userdict})

def delviewimg(request,pk):
    rid = ImageDetails.objects.get(id=pk)
    rid.delete()
    userdict = ImageDetails.objects.all()
    return render(request, 'original_img_list.html', {'userdict': userdict})


def compare(request,oimage,uimage):
    img1 = cv2.imread(oimage)
    img2 = cv2.imread(uimage)

    # convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # define the function to compute MSE between two images
    def mse(img1, img2):
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff ** 2)
        mse = err / (float(h * w))
        return mse, diff

    error, diff = mse(img1, img2)
    print("Image matching Error between the two images:", error)
    cv2.imshow("difference", diff)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return render(request, 'user_img_list.html')

def change_pass(request):
    username=request.session['username']
    if request.method=="POST":
        current_pass=request.POST.get("t1")
        new_pass=request.POST.get("t2")
        cofirm_pass=request.POST.get("t3")
        udata=UserLogin.objects.filter(username=username).filter(password=current_pass).count()
        if udata>=1:
            if new_pass==cofirm_pass:
                UserLogin.objects.filter(username=username).update(password=new_pass)
                return render(request,'user_home.html')
            else:
                return render(request,'change_password.html')
        else:
            return render(request, 'change_password.html')
    return render(request, 'change_password.html',{'username':username})

def uchange_pass(request):
    username=request.session['username']
    if request.method=="POST":
        current_pass=request.POST.get("t1")
        new_pass=request.POST.get("t2")
        cofirm_pass=request.POST.get("t3")
        udata=UserLogin.objects.filter(username=username).filter(password=current_pass).count()
        if udata>=1:
            if new_pass==cofirm_pass:
                UserLogin.objects.filter(username=username).update(password=new_pass)
                return render(request,'user_home.html')
            else:
                return render(request,'change_password.html')
        else:
            return render(request, 'change_user_pwd.html')
    return render(request, 'change_user_pwd.html',{'username':username})

def feedback(request):
    if request.method == "POST":
        s1 = request.POST.get('t1', '')
        s2 = request.POST.get('t2', '')
        s3 = request.POST.get('t3', '')
        s4 = request.POST.get('t4', '')
        Feedback.objects.create(from_details=s1, to=s2, date=s3, details=s4)
        return render(request, 'feedback.html')
    return render(request, 'feedback.html')

def showfeedback(request):
    userdict = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'userdict': userdict})
