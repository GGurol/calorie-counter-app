from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    pass

class GoalChoices(models.Model):
    goal_choice =models.CharField(max_length=20)

    def __str__(self):
        return self.goal_choice


class ActivityChoices(models.Model):
    activity_choice =models.CharField(max_length=20)

    def __str__(self):
        return self.activity_choice


class Nutrition(models.Model):
    carbs = models.IntegerField(default=40)
    protein =models.IntegerField(default=30)
    fat =models.IntegerField(default=30)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_created = models.BooleanField(default=False)
    your_goal = models.ForeignKey(GoalChoices, on_delete=models.CASCADE)
    start_weight= models.IntegerField()
    goal_weight= models.IntegerField()
    calorie_goal= models.IntegerField()
    activity= models.ForeignKey(ActivityChoices, on_delete=models.CASCADE)
    nutrition_goal= models.ForeignKey(Nutrition, on_delete=models.CASCADE, default=1500)
    
    def __str__(self):
        return f"{self.calorie_goal} to {self.your_goal}"


class Grocery(models.Model):
    grocery_name = models.CharField(max_length=30)
    grams = models.IntegerField()
    calorie = models.IntegerField()
    total_protein = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)
    dietary_fibers = models.FloatField(default=0)
    sugars = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)
    saturated_fat = models.FloatField(default=0)
    sodium = models.FloatField(default=0)

    def __str__(self):
        return self.grocery_name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField(help_text='Use line breaks to separate ingredients.')
    instructions = models.TextField(help_text='<br><br>')
    image_url = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.name

class Meal(models.Model):
    MEAL_TYPES = [
       ('Breakfast', 'Breakfast'),
       ('Lunch', 'Lunch'),
       ('Dinner', 'Dinner'),
    ]
    date = models.DateField()
    profile= models.ForeignKey(Profile, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    groceries= models.ManyToManyField(Grocery)
    
    def __str__(self):
        return self.meal_type


class MealGrocery(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    grocery = models.ForeignKey(Grocery, on_delete=models.CASCADE)
    updated_grams = models.IntegerField()  
    updated_calorie = models.FloatField(default=0)
    updated_total_protein = models.FloatField(default=0)
    updated_total_carbs = models.FloatField(default=0)
    updated_dietary_fibers = models.FloatField(default=0)
    updated_sugars = models.FloatField(default=0)
    updated_total_fat = models.FloatField(default=0)
    updated_saturated_fat = models.FloatField(default=0)
    updated_sodium =models.FloatField(default=0)


class Steps(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE) 
   add_steps = models.IntegerField(default=0)
   date = models.DateField(default=True)

class SuccessStories(models.Model):
    title_success= models.CharField(max_length=24)
    description= models.TextField()
    image_url_success = models.URLField(blank=True, null=True)  

    def __str__(self):
        return self.title_success

