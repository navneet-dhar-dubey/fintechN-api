### for Celery.
import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery import shared_task
from .models import Transaction

@shared_task
def send_monthly_summary_email(user_id):
    """
    A Celery task to generate and email a monthly summaryto a user.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "User not found."

    today = datetime.date.today()
    transactions = Transaction.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )

    total_income = transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expenses

    #prepare the email
    subject = f'Your Financial Summary for {today.strftime("%B %Y")}'
    message = f"""
    Hello {user.username},

    Here is your financial summary for this month:

    Total Income: ₹{total_income:,.2f}
    Total Expenses: ₹{total_expenses:,.2f}
    Net Balance: ₹{net_balance:,.2f}

    Thank you for using the Fintech API! (Powered by Dubey Industries :) )
    """
    from_email = 'noreply@fintechapi.com'
    recipient_list = [user.email] if user.email else []

    if recipient_list:
        send_mail(subject, message, from_email, recipient_list)
        return f"Summary email sent to {user.username}."
    else:
        return f"User {user.username} has no email address."
