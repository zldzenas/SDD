from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.context_processors import csrf
import sys
import datetime
from insurancePlan.models import *
from django.db.models import Max
from django.core.mail import send_mail
from django.db.models import Q


def login(request):
    # define the request of returning the Login page
    c = {}
    c.update(csrf(request))
    return render_to_response("Login.html",context_instance=RequestContext(request))

def signup(request):
    # define the request of returning the Signup page
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("Signup.html",context_instance=RequestContext(request))

def commonuserRecommend(request):
    # define the function of processing the common user recommend 
    if request.is_ajax():
        zipcode=request.GET['zip']
        planid=0
        # Search the plans according to the given zipcode.  Result contains at most 3 plans
        promotion_list=list(PromotionPlan.objects.filter(zipcode=zipcode).order_by('company_name')[0:3])
        html_string=""
        # show the results with a table
        html_string+="<table width=\"500\" border=\"3\">"
        html_string+="<tr><td class=\"FontsForTables\">Company Name</td><td class=\"FontsForTables\">Plan Name</td><td class=\"FontsForTables\">Coverage</td><td class=\"FontsForTables\">Rate</td></tr>"
        for i in promotion_list:
            html_string+="<tr><td>"
            html_string+=i.company_name
            html_string+="</td><td>"
            html_string+=i.plan_name
            html_string+="</td><td>"
            #p=Plan.objects.get(plan_name=i.plan_name)
            #r=Rate.objects.get(planid=p.pid)
            html_string+=str(i.coverage_time)
            html_string+=" months"
            html_string+="</td><td>"
            html_string+="$"
            html_string+=str(i.rates)
            html_string+="</td></tr>"           
        html_string+="</table>"
        message=html_string
    else:
        message="Not Ajax!"
    return HttpResponse(message)

def retrievePassword(request):
    # define the request of returning the RetrievePassword page
    return render_to_response("RetrievePassword.html")

def contactUs(request):
    # define the request of returning the ContactUs Page 
    return render_to_response("ContactUs.html")

def sendPassword(request):
    # define the function of sending password to user's email  
    email=request.GET['email']
    # if email doesn't exist, the app will alert message
    email=email.replace("%40","@").strip()
    password=User.objects.get(email=email).password
    message='Your old password is '+password+'. Now you can login in again.'
    x=send_mail('Soy Vey_Change your password',message,email,[email],fail_silently=False)
    return HttpResponse("Email has been sent!")

def resetPassword(request):
    # define the request of returning the ResetPassword Page 
    return render_to_response("ResetPassword.html")

def resetPassword2(request):
    # define the function of resetting password
    email = request.GET['email']
    p = User.objects.get(email=email)
    password = request.GET['password']
    if password == p.password:
        newpassword = request.GET['newpassword1']
        p.password = newpassword
        p.save()
    else:
        return HttpResponse("Sorry, the password is incorrect")
    return HttpResponse("Password has been resetted")

def advanceduserSearch(request):
    # define the request of returning the AdvancedSearch Page
    return render_to_response("AdvancedSearch.html")

def advanceduserSearch2(request):
    # define the function of AdvancedSearch
    if request.is_ajax():
        age=int(request.GET['age'])
        if age==0:
            p1=Plan.objects.all().filter(age__lte=24)
        elif age==2:
            p1=Plan.objects.all().filter(age__gte=30)
        else:
            p1=Plan.objects.all().filter(age__in=[25,26,27,28,29])
    
        rates=int(request.GET['rates'])
        if rates==0:
            p2=p1.filter(rates__lte=1000)
        elif rates==2:
            p2=p1.filter(rates__gte=1500)
        else:
            p2=p1.filter(Q(rates__lt=1500)&Q(rates__gt=1000))

        coverage_time=int(request.GET['coverage_time'])
        if coverage_time==0:
            p3=p2.filter(coverage_time=12)
        elif coverage_time==1:
            p3=p2.filter(coverage_time=11)
        elif coverage_time==2:
            p3=p2.filter(coverage_time=10)
        elif coverage_time==3:
            p3=p2.filter(coverage_time=9)
        elif coverage_time==4:
            p3=p2.filter(coverage_time=8)
        elif coverage_time==5:
            p3=p2.filter(coverage_time=7)
        elif coverage_time==6:
            p3=p2.filter(coverage_time=6)
        elif coverage_time==7:
            p3=p2.filter(coverage_time=5)
        elif coverage_time==8:
            p3=p2.filter(coverage_time=4)
        else:
            p3=p2.filter(coverage_time=3)


        benefit=int(request.GET['benefit'])
        if benefit==0:
            p4=p3.filter(lifetime_benefit_max__lte=100000)
        elif benefit==2:
            p4=p3.filter(lifetime_benefit_max__gte=150000)
        else:
            p4=p3.filter(Q(lifetime_benefit_max__lt=150000)&Q(lifetime_benefit_max__gt=100000))

        coverage_percent=int(request.GET['coverage_percent'])
        if coverage_percent==0:
            p5=p4.filter(percentage_within_network__lte=50)
        elif coverage_percent==2:
            p5=p4.filter(percentage_within_network__gte=75)
        else:
            p5=p4.filter(Q(percentage_within_network__lt=50)&Q(percentage_within_network__gt=75))

        care=int(request.GET['care'])
        if care==0:
            p6=p5.filter(preventive_care="yes")
        else:
            p6=p5.filter(preventive_care="no")

        repatriation=int(request.GET['care'])
        if repatriation==0:
            p7=p6.filter(repatriation="yes")
        else:
            p7=p6.filter(repatriation="no")
            
        condition=int(request.GET['care'])
        if condition==0:
            p8=p7.filter(preexisting_condition="yes")
        else:
            p8=p7.filter(preexisting_condition="no")
            
        dental=int(request.GET['dental'])
        if dental==0:
            p9=p8.filter(dental_coverage="yes")
        else:
            p9=p8.filter(dental_coverage="no")
            
        plan_list=list(p9.order_by('plan_name')[0:3])
        
        html_string=""
        html_string+="<table width=\"500\" border=\"3\">"
        html_string+="<tr><td class=\"FontsForTables\">Company Name</td><td class=\"FontsForTables\">Plan Name</td><td class=\"FontsForTables\">Coverage</td><td class=\"FontsForTables\">Rate</td></tr>"
        for i in plan_list:
            html_string+="<tr><td>"
            # if Plan has a foreign key reference to Company
            # c=Company.objects.filter(plan__companyid=i.companyid)
            # html_string+=c.company_name
            html_string+="United Healthcare"
            html_string+="</td><td>"
            html_string+=i.plan_name
            html_string+="</td><td>"
            #p=Plan.objects.get(plan_name=i.plan_name)
            #r=Rate.objects.get(planid=p.pid)
            html_string+=str(i.coverage_time)
            html_string+=" months"
            html_string+="</td><td>"
            html_string+="$"
            html_string+=str(i.rates)
            html_string+="</td></tr>"           
        html_string+="</table>"
        message=html_string
    else:
        message="Not Ajax!"
    return HttpResponse(message)
    
def advancedSearch(request):
    # define the function of signup
    c = {}
    c.update(csrf(request))
    uid=0
    email,password,firstname,lastname=request.POST['email'], request.POST['password'],request.POST['firstname'],request.POST['lastname']
    if not User.objects.all():
        uid=1
    else:
        #uid=uid+1
        uid=User.objects.all().aggregate(Max('uid'))['uid__max']+1
        #uid=User.objects.get().order_by("-uid")[0]+1
    User.objects.create(uid=uid,email=email,password=password,firstname=firstname,lastname=lastname)
    p1=User(uid=uid,email=email,password=password,firstname=firstname,lastname=lastname)
    p1.save()
    return render_to_response("AdvancedSearch.html",context_instance=RequestContext(request))

def advancedSearch2(request):
    # define the function of login
    c = {}
    c.update(csrf(request))
    email,password=request.POST['email'], request.POST['password']
    # print User.objects.filter(email==email,password==password)
    if User.objects.filter(email=email,password=password):        
        return render_to_response("AdvancedSearch.html",context_instance=RequestContext(request))
    else:
       
        html="<html><body>Login failed. The password and email don't match</body></html>"
        return HttpResponse(html)
    
def current_datatime(request):
    now=datetime.datetime.now()
    p2=Company(cid=1,name='UnitedHealth')
    p2.save()
    html="<html><body>It is now %s.</body></html>" % p2.name 
    return HttpResponse(html)

