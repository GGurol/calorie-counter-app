from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Profile, GoalChoices, ActivityChoices, Grocery, Nutrition, Recipe, User, Meal, SuccessStories

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'formatted_ingredients', 'instructions', 'image_url']

    def formatted_ingredients(self, obj):
        return mark_safe(obj.ingredients.replace('\n', '<br>'))
    formatted_ingredients.short_description = 'Ingredients'


admin.site.register(Profile)
admin.site.register(GoalChoices)
admin.site.register(ActivityChoices)
admin.site.register(Grocery)
admin.site.register(Nutrition)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(User)
admin.site.register(Meal)
admin.site.register(SuccessStories)
