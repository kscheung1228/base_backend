from django.contrib import admin

# Register your models here.

# class StepInline(admin.StackedInline):
#     model = Step
#     fk_name = "homework"
#     empty_value_display = '--empty--'

# class HomeworkAdmin(admin.ModelAdmin):
#     list_display = ('name','category','id','pk','hurdle_checkbox','hurdle')
#     empty_value_display = '--empty--'

#     fields = ('name','category','hurdle_checkbox','hurdle')

#     inlines = [
#         StepInline,
#     ]
# admin.site.register(Homework,HomeworkAdmin)

class BaseitemAdmin(admin.ModelAdmin):
    list_display = ('itemname','itemfile','id','pk')
    # empty_value_display = '--empty--'

    fields = ('itemname','itemfile','id','pk')

    # inlines = [
    #     StepInline,
    # ]
admin.site.register(BaseitemAdmin)