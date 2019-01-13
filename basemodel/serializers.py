from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Baseitem
# from steps.models import Step
# from steps.serializers import StepsModelSerializer
from drf_writable_nested import WritableNestedModelSerializer


# class StepsModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Step
#         fields = ('id','description','hyperlink','content','addedon','order','homework')
#         ordering = ('order' , )

class BaseitemsModelSerializer(serializers.ModelSerializer):

    # steps = serializers.SerializerMethodField()

    class Meta:
        model = Baseitem
        fields = ('id','itemfile','itemname')
     
    # def get_steps(self, instance):
    #     songs = instance.steps.all().order_by('order')
    #     return StepsModelSerializer(songs, many=True).data
