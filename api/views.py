from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .serializers import CategorySerializer, TransactionSerializer,UserSerializer, BudgetSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Category, Transaction, Budget
import datetime
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .filters import TransactionFilter
from rest_framework.filters import SearchFilter
import django_filters
from .tasks import send_monthly_summary_email
from django.views.decorators.csrf import csrf_exempt
import csv
from django.http import HttpResponse
from rest_framework_csv.renderers import CSVRenderer

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer
    permission_classes= [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(user= self.request.user)
    
    
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)
        
        
class TransactionViewSet(viewsets.ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes= [permissions.IsAuthenticated]
    filterset_class = TransactionFilter
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['description', 'category__name']
    
    
    def get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def monthly_summary(request):
    user= request.user
    today= datetime.date.today()
    
    transactions = Transaction.objects.filter(user=user, date__year=today.year, date__month=today.month)
    
    total_income= transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    
    net_balance= total_income-total_expenses
    
    summary_data={
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance
    }
    
    return Response(summary_data)



class UserCreateAPIView(generics.CreateAPIView):
    permission_classes= [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset=User.objects.all()
    
    

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def  get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        


    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def email_report_view(request):
    
    ## Triggers the task to send monthly summary email.
    
    user= request.user
    
    #.delay() sends the task to Celery.
    send_monthly_summary_email.delay(user.id)
    
    return Response(
        {
            'message': 'Your report is being generated and will be emailed to you. Dont Worry!!.'
        },
        status=202
    )
    
  
  
        
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
@renderer_classes([CSVRenderer])  
def export_transactions_csv(request):
    # generates and downloades a csv file of the user's transaction for the current month.
    
    
    user= request.user
    today=datetime.date.today()
    transactions = Transaction.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    ).order_by('date')
    
    
    # using our own serilizer for data formatting also
    serializer = TransactionSerializer(transactions, many=True)
    
    
    # for  downloading  file
    headers = {
        'Content-Disposition': f'attachment; filename="transactions_{today.strftime("%m-%Y")}.csv"'
    }
    
        
    return Response(serializer.data, headers=headers)
    