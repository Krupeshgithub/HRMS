from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,default="")
    phone = models.CharField(max_length=40)
    Employe_id = models.CharField(max_length=40)    
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=60,default="")
    puch_in = models.TimeField(blank=True,null=True)
    puch_out = models.TimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    logo = models.FileField(upload_to='media/images/',default='media/images/hrms.png')

    def __str__(self) :
            return self.name

class HR(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,null=True,default="")
    phone = models.CharField(max_length=40)
    Employe_id = models.CharField(max_length=40)    
    date = models.CharField(null=True,blank=True,max_length=50)    # kuch gadbad he!!!!!
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=60,default="")
    puch_in = models.TimeField(blank=True,null=True)
    puch_out = models.TimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    logo = models.FileField(upload_to='media/images/',default='media/images/hrms.png')
    # video = models.FileField(upload_to='/')


    def __str__(self) :
        return self.name

class Employe(models.Model):
    emp_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50,default="")
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True,default='')
    phone = models.CharField(max_length=40)
    date = models.DateField(null=True)
    role = models.CharField(max_length=20,blank=True,null=True)
    salary = models.CharField(max_length=40,null=True)
    password = models.CharField(max_length=60)
    Employe_id = models.CharField(max_length=40,default="")
    designation = models.CharField(max_length=50)
    puch_in = models.TimeField(blank=True,null=True)
    puch_out = models.TimeField(blank=True,null=True)
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    logo = models.FileField(upload_to='media/images/',default='media/images/hrms.png')


    def __str__(self) :
        return self.name


class Transaction(models.Model):
    made_by = models.ForeignKey(HR, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class Project(models.Model):
    
    # user_id = models.ForeignKey(HR,on_delete=models.CASCADE)
    Project_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    Priority = models.CharField(max_length=40,blank=True,null=True)
    Project_leader = models.CharField(max_length=60,blank=True)
    add_team1 = models.CharField(max_length=40)
    add_team2 = models.CharField(max_length=40)
    add_team3 = models.CharField(max_length=40)
    add_team4 = models.CharField(max_length=40)
    # is_verify = models.BooleanField(default=False)
    describe = models.TextField(max_length=300)
    logo = models.FileField(upload_to='media/document/',default='media/document/python_assignment_5PHX6G6.pdf')
    
    def __str__(self):
        return self.Project_name

class client_client(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=60)

     
    def __str__(self):
        return self.name

class file(models.Model):
    files = models.FileField(upload_to="media/document")

    # def whenpublished(self):
    #         now = timezone.now()

    #         diff=now - self.create_at

    #         if diff.days==0 and diff.seconds >= 0 and diff.seconds < 60:
    #             seconds = diff.seconds

    #             if seconds == 1:
    #                 return str(seconds) + "second ago"

    #             else:
    #                 return str(seconds) + "seconds ago"
    #         if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
    #             minutes = math.floor(diff.seconds/60)

    #             if minutes == 1:
    #                 return str(minutes) + " minute ago" 
    #             else:
    #                 return str(minutes) + " minutes ago"
    #         if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
    #             minutes = math.floor(diff.seconds/3600)

    #             if minutes == 1:
    #                 return str(minutes) + " day ago" 
    #             else:
    #                 self.food_status = "Expired"
    #                 self.save()
    #                 return str(minutes) + " days ago"
    #         if diff.days == 0 and diff.seconds >= 86400 and diff.seconds < 3156420:
    #             minutes = math.floor(diff.seconds/60)

    #             if minutes == 1:
    #                 return str(minutes) + " month ago" 
    #             else:
    #                 return str(minutes) + " month's ago"
