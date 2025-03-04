from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from Caloriecounter.models import Profile, Grocery, Nutrition, Recipe, GoalChoices, ActivityChoices, User, Meal, MealGrocery, Steps, SuccessStories
from django.db.models import F,Sum
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_date
import datetime

# Create your views here.
def index(request):
    stories = SuccessStories.objects.all()
    return render(request, 'caloriecounter/welcome.html',{
        "stories": stories
    })

# Login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "caloriecounter/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "caloriecounter/login.html")

# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "caloriecounter/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "caloriecounter/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "caloriecounter/create_profile.html")
    else:
        return render(request, "caloriecounter/register.html")

# Diary
def diary(request):
    if request.method == 'POST':
        selected_date_str = request.POST.get('selected_date')
        request.session['selected_date'] = selected_date_str
    else:
        selected_date_str = request.session.get('selected_date', datetime.date.today().strftime('%Y-%m-%d'))
    
    selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
    total_steps = Steps.objects.filter(user=request.user, date=selected_date).aggregate(Sum('add_steps'))['add_steps__sum'] or 0
    calories_burned = round(total_steps * 0.04) # Assuming 0.04 calories per step

    profile= Profile.objects.filter(user=request.user).first()
    if not profile:
        # Redirect to the welcome page or profile creation page
      return redirect('create_profile')
   
    nutrition_info = profile.nutrition_goal  
    calorie_goal= profile.calorie_goal
    carbs = nutrition_info.carbs * 0.01
    fat = nutrition_info.fat * 0.01
    protein = nutrition_info.protein * 0.01
    carbs_calories = round(carbs * calorie_goal)
    protein_calories = round(protein * calorie_goal)
    fat_calories = round(fat * calorie_goal)
    gram_of_carbs = round(carbs_calories / 4)
    gram_of_protein = round(protein_calories / 4)
    gram_of_fat = round(fat_calories / 7)
    calorie_goal= profile.calorie_goal

    # Sum of calories
    total_meal_calories = MealGrocery.objects.filter(
        meal__profile=profile, 
        meal__date=selected_date
    ).aggregate(Sum('updated_calorie'))['updated_calorie__sum'] or 0
    total_meal_calories = round(total_meal_calories)

    # Sum of macronutrients
    total_nutrients = MealGrocery.objects.filter(
        meal__profile=profile, 
        meal__date=selected_date
    ).aggregate(
        total_protein=Sum('updated_total_protein'),
        total_fat=Sum('updated_total_fat'),
        total_carbs=Sum('updated_total_carbs')
    )

    total_protein = round(total_nutrients['total_protein'] or 0)
    total_fat = round(total_nutrients['total_fat'] or 0)
    total_carbs = round(total_nutrients['total_carbs'] or 0)

    remaining_calories = calorie_goal - total_meal_calories + calories_burned
    calories_over = remaining_calories < 0  
    exceeded_calories = abs(remaining_calories) if calories_over else 0

    # Check calories for the day
    net_calories_consumed = total_meal_calories - calories_burned

    # Check if net calories consumed is greater than the goal
    calories_over = net_calories_consumed > calorie_goal

    #   Calculate exceeded or remaining calories
    exceeded_or_remaining_calories = abs(net_calories_consumed - calorie_goal)

    # Calculate percentage of goal reached
    calories_percentage = (net_calories_consumed / calorie_goal) * 100

    # Ensure the percentage is clamped between 0 and 100
    calories_percentage = max(min(calories_percentage, 100), 0)
    calorie_goal = profile.calorie_goal
    meal_calorie_goal = round(calorie_goal / 3)  # One-third for each meal

    # Calculate calories consumed for each meal
    breakfast_calories = round(MealGrocery.objects.filter(
        meal__profile=profile, 
        meal__date=selected_date, 
        meal__meal_type='Breakfast'
    ).aggregate(Sum('updated_calorie'))['updated_calorie__sum'] or 0)

    lunch_calories = round(MealGrocery.objects.filter(
        meal__profile=profile, 
        meal__date=selected_date, 
        meal__meal_type='Lunch'
    ).aggregate(Sum('updated_calorie'))['updated_calorie__sum'] or 0)

    dinner_calories = round(MealGrocery.objects.filter(
        meal__profile=profile, 
        meal__date=selected_date, 
        meal__meal_type='Dinner'
    ).aggregate(Sum('updated_calorie'))['updated_calorie__sum'] or 0)

    # Percentages for progress bar
    breakfast_percentage = (breakfast_calories / meal_calorie_goal * 100) if meal_calorie_goal > 0 else 0
    lunch_percentage = (lunch_calories / meal_calorie_goal * 100) if meal_calorie_goal > 0 else 0
    dinner_percentage = (dinner_calories / meal_calorie_goal * 100) if meal_calorie_goal > 0 else 0
    carbs_percentage = ( total_carbs / gram_of_carbs * 100) if gram_of_carbs > 0 else 0
    protein_percentage = (total_protein / gram_of_protein * 100) if gram_of_protein > 0 else 0
    fat_percentage = (total_fat / gram_of_fat * 100) if gram_of_fat > 0 else 0

    return render(request, 'caloriecounter/diary.html',{
        "gram_of_protein": gram_of_protein,
        "gram_of_fat" : gram_of_fat,
        "gram_of_carbs": gram_of_carbs,
        "carbs_calories" : carbs_calories,
        "protein_calories": protein_calories,
        "fat_calories" : fat_calories,
        "remaining_calories": remaining_calories,
        "calories_over": calories_over,
        "exceeded_calories": exceeded_calories,
        'steps': steps,
        'calories_burned': calories_burned,
        "selected_date": selected_date,
        "total_klc": total_meal_calories,
        "total_protein": total_protein,
        "total_fat": total_fat,
        "total_carbs": total_carbs,
        "breakfast_calories": breakfast_calories,
        "lunch_calories": lunch_calories,
        "dinner_calories": dinner_calories,
        "meal_calorie_goal": meal_calorie_goal,
        'breakfast_percentage': breakfast_percentage,
        'lunch_percentage': lunch_percentage,
        'dinner_percentage': dinner_percentage,
        'carbs_percentage': round(carbs_percentage, 2),
        'protein_percentage': round(protein_percentage, 2),
        'fat_percentage': round(fat_percentage, 2),
        "calories_percentage": calories_percentage, 
    })
 
# Create profile
def create_profile(request):
    if request.method == "POST":
        user = request.user
        profiles= Profile.objects.all()
        your_goal = request.POST.get('goals')
        start_weight= int(request.POST.get('start_weight'))
        goal_weight= int(request.POST.get('goal_weight'))
        activity= request.POST.get('activity')
        calorie_goal = int(request.POST.get('calorie_goal'))
        carbs = int(request.POST.get('carbs'))
        protein = int(request.POST.get('protein'))
        fat = int(request.POST.get('fat'))
        goal_object = GoalChoices.objects.filter(goal_choice__iexact=your_goal).first()
        activity_object = ActivityChoices.objects.filter(activity_choice__iexact=activity).first()

        nutrition = Nutrition(
            carbs=carbs, 
            protein=protein, 
            fat=fat)
        nutrition.save()

        profile = Profile(
            user = user,
            your_goal = goal_object,
            start_weight = start_weight,
            goal_weight = goal_weight,
            calorie_goal = calorie_goal,
            activity = activity_object,
            nutrition_goal = nutrition)
        profile.save()

        return redirect('diary')
    else:
        return render(request, 'caloriecounter/create_profile.html')

# Profile
def view_profile(request):
    activity = ActivityChoices.objects.all()
    profile = Profile.objects.filter(user=request.user).first()
    # If no profile, redirect to create profile page
    if not profile:
        return redirect('create_profile')  

    nutrition_info = profile.nutrition_goal
    your_goal= profile.your_goal
    start_weight = round(profile.start_weight)
    goal_weight = round(profile.goal_weight)
    calorie_goal = profile.calorie_goal
    activity = profile.activity
    carbs = nutrition_info.carbs 
    fat = nutrition_info.fat 
    protein = nutrition_info.protein 

    BASELINE_CALORIES = 2000  # Example baseline

    # Calculate estimated maintenance calories based on activity level
    if profile.activity.activity_choice == 'High':
       maintenance_calories = BASELINE_CALORIES * 2.0
    elif profile.activity.activity_choice == 'Moderate':
       maintenance_calories = BASELINE_CALORIES * 1.5
    else:  # Assuming 'low' or any other activity level
       maintenance_calories = BASELINE_CALORIES

    # Calculate Daily Calorie Deficit/Surplus
    daily_calorie_difference = calorie_goal - maintenance_calories

    # Proceed with the usual calculation
    weekly_weight_change = abs(daily_calorie_difference) * 7 / 7700
    total_weight_change = abs(goal_weight - start_weight)

    if profile.start_weight == profile.goal_weight:
        message = "Your current weight matches your goal weight. Focus on maintaining your current healthy habits."
    else:
        # Calculate Daily Calorie Deficit/Surplus
        daily_calorie_difference = profile.calorie_goal - maintenance_calories
        weekly_weight_change = abs(daily_calorie_difference) * 7 / 7700
        total_weight_change = abs(profile.goal_weight - profile.start_weight)

        if weekly_weight_change != 0:
            estimated_weeks = int(total_weight_change / weekly_weight_change)
            message = f"It will take approximately {estimated_weeks} weeks to reach your goal weight."
        else:
            message = "Indeterminate time to reach goal weight."

    return render(request, 'caloriecounter/profile.html',{
        "fat" : fat,
        "protein": protein,
        "carbs" : carbs,
        "calorie_goal" : calorie_goal,
        "your_goal": your_goal,
        "start_weight": start_weight,
        "goal_weight": goal_weight,
        "activity": activity,
        "message": message, 
       
    })

# Edit profile
def edit_profile(request):
    profile = Profile.objects.get(user=request.user) 
    nutrition = Nutrition.objects.get(profile=profile) # Get the profile for the logged-in user
    goals = GoalChoices.objects.all()
    activity = ActivityChoices.objects.all()
    
    # Update and save values
    if request.method == 'POST':
        goal_choice = request.POST.get('goals')
        selected_goal_choice = GoalChoices.objects.get(goal_choice=goal_choice)
        profile.your_goal = selected_goal_choice
        activity_choice = request.POST.get('activity')
        selected_activity_choice = ActivityChoices.objects.get(activity_choice=activity_choice)
        profile.activity = selected_activity_choice
        profile.start_weight = round(float(request.POST.get('start_weight')), 0)
        profile.goal_weight = round(float(request.POST.get('goal_weight')), 0)
        profile.calorie_goal = round(float(request.POST.get('calorie_goal')), 0)
        nutrition.carbs = round(float(request.POST.get('carbs')), 0)
        nutrition.protein = round(float(request.POST.get('protein')), 0)
        nutrition.fat = round(float(request.POST.get('fat')), 0)
        
        nutrition.save()
        profile.save()
        return redirect('view_profile')

    # If it's a GET request, display the form with prepopulated data
    return render(request, 'caloriecounter/edit_profile.html', {
        'profile': profile,
        "goal_choices": goals,
        "activity_choices": activity
        })

# List of recipes
def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'caloriecounter/recipe_list.html', {
        'recipes': recipes
    })

# Fasting page
def fasting(request):
    return render(request, 'caloriecounter/fasting.html')


# Search groceries from database
def grocery_search(request):
    search_performed = False
    groceries = Grocery.objects.all()
    meal_type = request.GET.get('meal_type', '')
    query = request.GET.get('query', '')
    selected_date_str = request.GET.get('date', '')
    selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
    
    # Substring search
    if query:
        search_performed = True
        groceries = groceries.filter(grocery_name__icontains=query)  
    else:
        groceries = Grocery.objects.none() 

    return render(request, 'caloriecounter/grocery_list.html', {
        'groceries': groceries,
        'search_performed': search_performed,
        'query': query,
        'meal_type': meal_type,
        'selected_date': selected_date
    })

# Add grocery to meal
def add_meal(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user) 
        grocery_id = request.POST.get('grocery_id')
        meal_type = request.POST.get('meal_type')
        grocery = get_object_or_404(Grocery, id=grocery_id)
        selected_date_str = request.POST.get('selected_date')
        selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
        grams = request.POST.get('updated_grams') 
     
        # List of nutrient fields
        nutrients = ['calorie', 'total_protein', 'total_carbs', 'dietary_fibers', 'sugars', 'total_fat', 'saturated_fat', 'sodium', 'grams']

        # Updating an existing MealGrocery table
        meal_grocery_id = request.POST.get('meal_grocery_id')
        if meal_grocery_id:
            meal_grocery = MealGrocery.objects.get(id=meal_grocery_id)
            meal = meal_grocery.meal
        else:
            meal = Meal(profile=profile, meal_type=meal_type, date=selected_date)
            meal.save()
            meal_grocery = MealGrocery(meal=meal, grocery=grocery)

        # Update nutrient values
        for nutrient in nutrients:
            nutrient_key = f'updated_{nutrient}'
            nutrient_value_str = request.POST.get(nutrient_key, '0')
            nutrient_value = float(nutrient_value_str) if nutrient_value_str else 0
            setattr(meal_grocery, nutrient_key, nutrient_value)
        
        meal_grocery.save()

        redirect_url = reverse('show_meal') + f'?meal_type={meal_type}&date={selected_date.strftime("%Y-%m-%d")}'
        return HttpResponseRedirect(redirect_url)
    else:
        # Handle GET request
        meal_grocery_id = request.GET.get('meal_grocery_id')
        selected_date_str = request.GET.get('selected_date', '')
        selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
        meal_type = request.GET.get('meal_type', '')

        if meal_grocery_id:
            meal_grocery = get_object_or_404(MealGrocery, pk=meal_grocery_id)
            grocery = meal_grocery.grocery
       
        return render(request, 'caloriecounter/grocery_detail.html', {
            'grocery': grocery,
            'meal_grocery': meal_grocery,
            'meal_type': meal_type,
            'selected_date': selected_date,
        })

# Show single grocery
def grocery_detail(request,grocery_id):
    if request.method == 'GET':  
       grocery = Grocery.objects.get(pk=grocery_id)
       meal_type = request.GET.get('meal_type', '').strip() 
       selected_date_str = request.GET.get('date', '')
       selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()

    return render(request, 'caloriecounter/grocery_detail.html', {
        "grocery": grocery,
        "meal_type": meal_type,
        "selected_date": selected_date
    })

# Show specific meal
def show_meal(request):
    profile = Profile.objects.get(user=request.user) 
    selected_date_str = request.GET.get('date', '')
    selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
    meal_type = request.GET.get('meal_type', '')  # Get the meal type from the query parameters
    meal_groceries = MealGrocery.objects.filter(meal__meal_type=meal_type, meal__profile=profile, meal__date=selected_date)
    
    # Sum of macronutrients and calories in a meal
    total_nutrients = meal_groceries.aggregate(
        total_calories=Sum('updated_calorie'),
        total_grams=Sum('updated_grams'),
        total_protein=Sum('updated_total_protein'),
        total_fat=Sum('updated_total_fat')
    )
  
    return render(request, 'caloriecounter/show_meal.html', {
        'meal_groceries': meal_groceries,
        'meal_type': meal_type,  
        'selected_date': selected_date,
        'total_calories': round(total_nutrients['total_calories'] or 0),
        'total_grams': round(total_nutrients['total_grams'] or 0),
        'total_protein': round(total_nutrients['total_protein'] or 0),
        'total_fat': round(total_nutrients['total_fat'] or 0),
    
    })
  
# Delete grocery
def delete_meal_grocery(request, meal_grocery_id):
    meal_grocery = get_object_or_404(MealGrocery, pk=meal_grocery_id)
    meal_type = request.GET.get('meal_type', 'default_meal_type')
    selected_date = request.GET.get('date', 'default_date')
    meal_grocery.delete()

    redirect_url = reverse('show_meal') + f'?meal_type={meal_type}&date={selected_date}'
    return redirect(redirect_url)

# Add activity
def steps(request):
    if request.method == 'POST':
        selected_date_str = request.POST.get('selected_date')
    else:
        selected_date_str = request.GET.get('selected_date', datetime.date.today().strftime('%Y-%m-%d'))
    selected_date = parse_date(selected_date_str) if selected_date_str else datetime.date.today()
    
    if request.method == "POST":
        steps_count = int(request.POST.get('steps', 0))
        user_steps = Steps(user=request.user, add_steps=steps_count, date=selected_date)
        user_steps.save()

        return redirect('diary')  
    else:
    # Handle GET request to display steps for selected date
       total_steps = Steps.objects.filter(user=request.user, date=selected_date).aggregate(Sum('add_steps'))['add_steps__sum']
       steps_count = total_steps if total_steps is not None else 0

    return render(request, 'caloriecounter/add_steps.html', {
        "steps": steps_count,
        "selected_date": selected_date
    })



