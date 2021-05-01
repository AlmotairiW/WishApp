from django.db import models
import re
class UserManager(models.Manager):

    def reg_validator(self, postData):

        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

        if postData['fname'] =="":
            errors['fname'] = "First Name must be provided!"
        elif len(postData['fname']) < 2:
            errors['fname'] = "First Name should be at least 2 characters long"

        if postData['lname'] =="":
            errors['lname'] = "Last Name must be provided!"
        elif len(postData['lname']) < 2:
            errors['lname'] = "Last Name should be at least 2 characters long"
            
        if postData['email'] == "":
            errors['email'] = "Email must be provided!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid e-mail address!"
        elif User.objects.filter(email = postData['email']).exists():
            errors['email'] = "The email is already registered! go to log in :)"

        if postData['pass'] == "":
            errors['pass'] = "Password must be provided!"
        elif len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 charachters long"

        elif postData['pass_c'] == "":
            errors['pass_c'] = "Please confirm password"
        elif postData['pass'] != postData['pass_c']:
            errors['pass_c'] = "Password does not match!"
        
        return errors
        
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')
        if postData['email'] == "":
            errors['email'] = "Email must be provided!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid e-mail address!"
        elif not User.objects.filter(email = postData['email']).exists():
            errors['email'] = "The email is not registered! go to registeration :)"
        elif postData['pass'] =="":
            errors['pass'] = "Password must be provided!"
        elif len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 charachters long"
    
        return errors

class WishManager(models.Manager):

    def wish_validator(self, postData):
        errors = {}

        if postData['item'] == "":
            errors['item'] = "A wish must be provided!"
        elif len(postData['item']) < 3:
            errors['item'] = "A wish must consist of at least 3 characters!"

        if postData['desc'] == "":
            errors['desc'] = "A description must be provided!"
        elif len(postData['desc']) < 3:
            errors['desc'] = "A description must consist of at least 3 characters!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 50)
    password =  models.CharField(max_length = 50)
    objects = UserManager()

    #date & time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wish(models.Model):
    item = models.CharField(max_length = 255)
    description = models.TextField()
    wisher = models.ForeignKey(User, related_name="wishes", on_delete= models.CASCADE)
    is_granted = models.BooleanField()
    liked_by = models.ManyToManyField(User, related_name = "likes")
    objects = WishManager()
    #date & time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


