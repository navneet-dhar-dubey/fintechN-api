from rest_framework import serializers
from .models import Category, Transaction, User, Budget



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        
        
            # --- TEMPORARY DEBUGGING ---
            
        received_password = validated_data['password']
        print("---------------------------------------------------------")
        print(f"DEBUG: Registering user '{validated_data['username']}' with password: '{received_password}'")
        print("---------------------------------------------------------")
        # --------------------------
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        return user


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']
    
    
class TransactionSerializer(serializers.ModelSerializer):
    category_name= serializers.SerializerMethodField()
    
    class Meta:
        model= Transaction
        fields = ['id','user', 'category_name', 'category', 'amount', 'date', 'type']
        read_only_fields= ['user', 'category_name']
        
    def get_category_name(self, obj):
        """
        Returns the name of the category for the given transaction object.
        """
        # obj is the Transaction instance. We can access its related category's name.
        return obj.category.name if obj.category else None
    
    
    
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'amount', 'start_date', 'end_date']
        read_only_fields = ['user']
            