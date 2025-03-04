# Calorie Counting App NUNTRICOUNT

#### Video Demo: https://youtu.be/qVrzm_GttPs

#### Description:

    NutriCount is more than just a calorie tracker. It's a complete guide for anyone's nutrition and fitness journey.
    It does not just count calories. It looks at the whole picture of your health. 
    It combines keeping track of your diet, your exercise, and your personal health goals all in one place.


#### Distinctiveness and Complexity:

##### Unique and Complex Features

###### Personalized Nutritional Goals:
       Users can set specific objectives (like weight loss, muscle gain..) and define their macronutrient ratios. 
       This customization lets you create a diet plan that suits your specific dietary needs and preferences.

###### Dynamic Goal Tracking: 
       Based on the user's profile data, including starting and target weight, daily calorie goals, and activity levels, 
       the app calculates an estimated time to reach their goal weight. 
       This feature adds a layer of motivation and personalized planning to the user's journey.

###### Comprehensive Meal and Exercise Diary: 
       The app allows users to log meals and physical activities. It dynamically calculates and displays the intake of 
       macronutrients and calories per meal, providing real-time feedback on daily goals.
       The integration of a grocery database for meal planning further enhances its utility.

###### Activity Tracking and Caloric Adjustment:
       Users can log daily activities like steps taken, which the app converts into calories burned. 
       This data adjusts the remaining daily calorie allowance, displayed through dynamic progress bars for an intuitive 
       visual representation of daily goals versus actual intake and activity.

###### Fasting Tracker with Stopwatch: 
        Unique to NutriCount is the integration of a fasting tracker, complete with a stopwatch feature. 
        This caters to users who incorporate fasting into their health regimen, 
        providing them with a tool to monitor and manage fasting periods effectively.

###### Responsive and Adaptive UI: 
        The user interface is designed to be responsive and adaptive, making it easy and engaging for users to input data, 
        track their progress, and adjust their goals as needed.

##### Technical Complexity

    The app's sophistication lies in its blend of advanced features and user-centric design. 
    Key aspects like the algorithm for goal weight projection, interactive progress bars for macronutrients and calorie 
    tracking, and a comprehensive database, showcase its technical complexity.
    Adding to this is the date selection functionality which offers users the flexibility to monitor their dietary progress 
    on a specific day-by-day basis.
    This combination of intricate backend logic and a thoughtfully structured database ensures both precision and a 
    seamless user experience.


#### Including files:

##### BACKEND:
    - views.py
    - models.py
    - urls.py
    - admin.py
##### FRONTEND: 
    - templates
    - static

#### views.py includes:

    - User Authentication and Management: Incorporates routes for user registration (register), login (login_view), 
    and logout (logout_view). 
    These views handle user authentication and maintain session integrity.

    - Profile Management: The create_profile, view_profile, and edit_profile routes enable users to create, view, 
    and modify their nutritional profiles. 
    Users can set goals, start and target weights, daily calorie targets, and macronutrient preferences.

    - Dynamic Diary Management: The diary view dynamically calculates and displays daily nutrition and exercise data. 
    It includes complex calculations for macronutrient intake, calorie goals, and activity tracking, adjusting for calories 
    burned through steps.

    - Comprehensive Meal Logging: Integrates a meal diary where users can add and track meals (add_meal and show_meal). 
    It connects with a grocery database, allowing users to select and log groceries per meal, date-wise.

    - Steps Tracking: The steps view provides functionality for users to log their daily steps, 
    contributing to their activity level and caloric expenditure calculations

    - Data Integrity and Validation: Implements robust form validations and error handling to ensure data integrity 
    and user-friendly feedback.

    - Fasting Tracker: Includes a fasting tracker (fasting) with a simple, user-friendly interface.

    - Recipe and Grocery Management: Features views like recipes and grocery_search for accessing and managing recipes
    and grocery data.

    - Nutrient and Calorie Calculations: Employs intricate logic to calculate and display nutritional information, 
    including macronutrient breakdowns and calorie counts.

    - Date-wise Tracking: Allows users to select specific dates for meal and step tracking.

#### urls.py includes:

    Each path is linked to a specific view in the views.py file, which handles the logic and rendering of the corresponding 
    web pages. 
    This setup provides a structured and organized approach to navigating and utilizing the various features of the 
    nutrition and fitness tracking app.

#### models.py includes:

    Each class represents a different aspect of the app's data model.

      - User: Extends Django's AbstractUser to incorporate custom user functionality

      - GoalChoices: Represents different user goals (like weight loss, muscle gain..)

      - ActivityChoices: Stores activity levels (low, moderate, high)

      - Nutrition: Keeps track of macronutrient ratios (carbs, protein, fat) as integer percentages

      - Profile: Links to a User instance and stores the user’s fitness goals, weight details, calorie goals, activity level
      and nutritional goals

      - Grocery: Contains detailed nutritional information for different grocery items, including protein, carbs, fats,
      and other dietary elements

      - Recipe: Stores recipes

      - Meal: Represents different meal types (Breakfast, Lunch, Dinner) with a date, profile link, and associated groceries

      - MealGrocery: Connects meals to specific grocery and includes detailed nutritional information based on portion size

      - Steps: Tracks the number of steps taken by a user on a particular date

      - SuccessStories: Captures user success stories

#### templates insludes:
     
    The templates directory contains several HTML templates, each serving a specific function in the user interface. 
    Here's a brief overview:

      - layout.html: A base template that includes elements like the navigation bar, stylesheet links, and scripts. 
      Other templates extend this base layout to maintain a consistent look and feel across the app

      - login.html: Provides a user interface for logging into the app

      - register.html: Allows new users to create an account

      - welcome.html (index page): Serves as the landing page, welcoming users to NutriCount. 
      It features success stories to motivate new users

      - recipes.html: Displays a collection of recipes

      - fasting.html: Dedicated to fasting tracking, this template includes a stopwatch feature and information
      on various fasting methods

      - create_profile.html: Enables new users to set up their profile

      - view_profile.html: Displays the user's profile informations
  
      - edit_profile.html: Allows users to update their profile details

      - grocery_list.html & grocery_detail.html: These templates are involved in managing grocery lists and detailed 
      views of each grocery item

      - show_meal.html: Used for displaying meals with the ability to add, edit or delete meal items

      - add_steps.html: Allows users to log their daily steps as part of their activity tracking

#### static includes:

##### JAVASCRIPT:

    Javascript part contributes to a more engaging, intuitive, and user-friendly experience. 
    It includes several key features:

      - Nutrition Goal Sum Calculation: Automatically calculates and updates the sum of macronutrient percentages 
      (carbs, protein, fat) to guide users in setting balanced nutrition goals

      - Fasting Stopwatch: Implements a timer for users engaging in fasting, with start, stop, and reset functionalities. 
      It stores fasting session data locally and displays   fasting duration upon completion

      - Dynamic Nutrition Value Adjustment: Adjusts nutritional values in real-time based on the grams of groceries input, 
      ensuring accurate tracking of caloric and macronutrient intake.

      - Date Handling for Diary: Enables users to select and submit dates, facilitating the tracking of meals and
      activities for specific days

      - Expandable Recipe and Fasting Method Details: Provides interactive "Read More" functionality for recipes and
      fasting methods, allowing users to view additional information in a user-friendly format

##### CSS:

    The CSS file provides the styling details that define a modern look, using a dark color scheme with white text
    for high contrast and readability.
    It includes customized styling for forms, navigation, and content areas, ensuring a consistent and responsive 
    user experience across various devices. 

#### How to run NutriCount?
     
    Set Up the Environment:
      - Install Django- pip install django
      - Clone the repository using git clone [https://github.com/me50/martina860/capstone.git]
      - Navigate to the project directory and run python manage.py migrate to set up the database schema
      - Run the Development Server:
        - Start the Django development server by running python manage.py runserver
        - This will host the app locally, typically at http://127.0.0.1:8000/








