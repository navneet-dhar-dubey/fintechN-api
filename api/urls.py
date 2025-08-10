from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, monthly_summary, BudgetViewSet, email_report_view, export_transactions_csv


router=DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')


urlpatterns = [
    # Custom, specific paths go FIRST
    path('summary/', monthly_summary, name='monthly-summary'),
    path('reports/email-summary/', email_report_view, name='email-summary'),
    path('transactions/export/', export_transactions_csv, name='export-transactions'),
    
    # The general, router-generated paths go LAST
    path('', include(router.urls)),
]
