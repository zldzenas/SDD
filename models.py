from django.db import models

# Create your models here.

class Company(models.Model):
    cid=models.IntegerField(primary_key=True)
    company_name=models.CharField(max_length=50)
    def __unicode__(self):
        return self.cid

class Plan(models.Model):
    pid=models.IntegerField(primary_key=True)
    companyid=models.IntegerField()
    userkindid=models.IntegerField()
    plan_name=models.CharField(max_length=50)
    coverage_time=models.IntegerField()
    lifetime_benefit_max=models.IntegerField()
    deductible=models.IntegerField()
    percentage_within_network=models.CharField(max_length=10)
    percentage_outof_network=models.CharField(max_length=10)
    outof_pocket_max=models.IntegerField()
    preventive_care=models.CharField(max_length=3)
    repatriation=models.CharField(max_length=3) 
    preexisting_condition=models.CharField(max_length=3)
    dental_coverage=models.CharField(max_length=3)
    url=models.CharField(max_length=100)
    age=models.IntegerField()
    rates=models.IntegerField()
    def __unicode__(self):
        return self.pid
    
    
class Rate(models.Model):
    rid=models.IntegerField(primary_key=True)
    companyid=models.IntegerField()
    planid=models.IntegerField()
    userkindid=models.IntegerField()
    age=models.IntegerField()
    coverage_time=models.IntegerField()
    rates=models.IntegerField()
    def __unicode__(self):
        return self.rid
    
class Userkind(models.Model):
    ukid=models.IntegerField(primary_key=True)
    userkind=models.CharField(max_length=20)
    def __unicode__(self):
        return self.ukid

class User(models.Model):
    uid=models.IntegerField(primary_key=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    def __unicode__(self):
        return self.uid

class PromotionPlan(models.Model):
    zipcode=models.IntegerField()
    plan_name=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
    coverage_time=models.IntegerField()
    rates=models.IntegerField()
    def __unicode__(self):
        return self.zipcode

class UserInsuranceList(models.Model):
    uid=models.IntegerField(primary_key=True)
    pid=models.IntegerField()
    def __unicode__(self):
        return self.uid
    
    
