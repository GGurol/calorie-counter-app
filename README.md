## 🥗 NutriCount - Calorie Counting App

#### 🔗 Live Demo: [Try the App Here]([https://your-deployment-link.com)](https://calorie-counter-app-urlp.onrender.com)

---

### 📜 Overview

NutriCount is a calorie and nutrition tracking web application that helps users monitor their daily food intake, track their physical activity, set goals, and manage their meals. Users can log meals, track macronutrients, set calorie targets, and even follow intermittent fasting routines.

---

### 🚀 Features

✅ **User Authentication** - Register, log in, and manage your profile

✅ **Food Diary** - Log and track meals with calorie and macronutrient breakdown

✅ **Activity Tracking** - Record daily steps and calories burned

✅ **Goal Setting** - Define weight goals and activity levels

✅ **Intermittent Fasting Timer** - Start, stop, and track fasting periods

✅ **Recipe Collection** - Browse and manage healthy recipes

✅ **Meal Planning** - View and adjust daily meal breakdowns

✅ **Watchlist for Groceries** - Save favorite groceries for easy access

---

### 🛠️ Installation & Setup

Clone the repository
```sh
git clone https://github.com/Martina-Talan/NutriCount.git
cd NutriCount
```

Install dependencies:
```sh
pip install -r requirements.txt
```
Apply database migrations:
```sh
python manage.py makemigrations Caloriecounter
python manage.py migrate
```
Create a superuser (optional for admin access):
```sh
python manage.py createsuperuser
```
Start the development server:
```sh
python manage.py runserver
```

---

### 📌 Usage

✅ **Register/Login** - Create an account and sign in

✅ **Create Profile** - Set your weight goal, activity level, and nutrition distribution

✅ **Track Calories & Meals** - Log daily meals, track calories, and macronutrient intake

✅ **Record Steps & Burned Calories** - Add steps to calculate calories burned

✅ **View and Edit Profile** - Update weight goals, calorie targets, and activity levels

✅ **Use Intermittent Fasting Timer** - Start and track fasting sessions

✅ **Browse & Add Recipes** - Discover meal ideas and add them to your plan

✅ **Grocery Search & Watchlist** - Search and save food items for meal planning

✅ **Check Nutrition Breakdown** - View detailed macronutrient reports

---

### 🔗 API Routes

| Method  | Endpoint                          | Description                          |
|---------|-----------------------------------|--------------------------------------|
| GET     | `/diary`                          | View daily food diary               |
| GET     | `/recipes`                        | Fetch all available recipes         |
| POST    | `/grocery_search`                 | Search for grocery items            |
| POST    | `/add_meal`                       | Add a food item to a meal           |
| POST    | `/steps`                          | Log steps to track calories burned  |
| GET     | `/fasting`                        | Track intermittent fasting progress |
| GET     | `/view_profile`                   | View user profile details           |
| POST    | `/create_profile`                 | Create a new user profile           |
| PUT     | `/edit_profile`                   | Update user profile settings        |
| DELETE  | `/delete_meal_grocery/<int:id>`   | Remove an item from a meal          |


---

### 🛠️ Technologies Used

- __Django__ – Backend framework

- __JavaScript__ – Interactive frontend logic

- __HTML & CSS__ – UI structure and styling

- __Bootstrap__ – Responsive design

---

### 🏆 Acknowledgments

This project was developed as part of the Harvard CS50W: Web Programming with Python and JavaScript course.
