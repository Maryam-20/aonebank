from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aonebank.transactionapp.models import Account_table, Transaction_table
from django.contrib import messages
from .forms import Account_Open_form, changePin_form, PinAuthentication_form, Transaction_form, Transaction_historyForm
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import timezone
from django.db import transaction
from django.db.models import F
import json
from urllib.parse import unquote

# Create your views here.
@login_required
def create_newAccount(request, userId):
    if request.method == "POST":
        account_form = Account_Open_form(request.POST)
        if account_form.is_valid():
            add_user = account_form.save(commit = False)
            add_user.user_id = userId
            add_user.save()
            
            messages.success(request, ("Account created succesffully"))
            return HttpResponsePermanentRedirect(reverse("profile", args=(userId)))
        
        else:
            messages.error(request, ("Please correct the error below."))
            return HttpResponsePermanentRedirect(reverse("new_account", args=(userId)))
    else:
        account_form = Account_Open_form()
        return render(request, "transactionapp/account_open_form.html", {"form": account_form})

@login_required
def displayMyAccount(request, userId):
    my_account = Account_table.objects.all().filter(user_id = userId)
    return render(request, "transactionapp/display_account.html", {"my_account": my_account})



@login_required
def changePin(request, accId):
    if request.method == "POST":
        change_pin_form = changePin_form(request.POST)
        if change_pin_form.is_valid():
            oldPin = change_pin_form.cleaned_data['oldPin']
            newPin1 = change_pin_form.cleaned_data['newPin1']
            newPin2 = change_pin_form.cleaned_data['newPin2']
            
            user_account = Account_table.objects.filter(account_id = accId, account_pin = oldPin).values()
            
        if user_account and newPin1 == newPin2:
            Account_table.objects.filter(account_id =accId).update(account_pin = newPin1)
            messages.success(request, ("Account pin updated successfully."))
            return HttpResponsePermanentRedirect(reverse('my_Account', args=(accId,)))
        
        else:
            messages.error(request, ("Your account number and pin does not match. Please, check and try again."))
            return HttpResponsePermanentRedirect(reverse('change_pin', args= (accId, )))
    
    else:
        change_pin_form = changePin_form()
        return render(request, "transactionapp/change_pin_form.html", {"change_pinForm": change_pin_form })
    
            
@login_required
def resetPin(request, accId, userId):
    Account_table.objects.filter(account_id = accId).update(account_pin = 0000)
    account = Account_table.objects.get(account_id = accId)
    
    # send email to the customer
    "Pin reset update", #Subject of the mail
    f'Dear customer your account {account.account_number} pin has ben reset succesfully. Your new pin is 0000'
    "aonebank@gmail.com" #from email (sender)
    [account.user.email], #To email (receiver)
    fail_silently =False, #Handle any error
    
    
    return HttpResponsePermanentRedirect(reverse("my_Account", args= (userId, )))

def pinAunthentication(request, action):
    account_list = [("", "Select account Number"),]
    account_num =Account_table.objects.all().filter(user_id = request.user.id).values()
    for account in account_num:
        account_list.append((account["account_number"], account["account_number"]))
        
    if request.method == "POST":
        pin_form = PinAuthentication_form(request.POST, account_list = account_list)
        if pin_form.is_valid():
            acc_number = pin_form.cleaned_data['account_number']
            acct_pin = pin_form.cleaned_data['pin']
        try:   
            user_account = Account_table.objects.get(account_number = acc_number, account_pin = acct_pin)
        
            return HttpResponsePermanentRedirect(reverse("transaction", args=(user_account.account_id, action )))
            
        except:
                messages.error(request, ("Your account number and pin do not match"))
                return HttpResponseRedirect("pin_auth")
        
            
    else:
        pin_form = PinAuthentication_form(account_list = account_list)
        return render(request, 'transactionapp/pin_auth_form.html', {'pin_form': pin_form, } )

@login_required
def userTransaction(request, accId, action):
    if request.method == "POST":
        exclude_fields = []
        
        if action == "deposit":
            exclude_fields = ["user", "account", "transaction_type","beneficiary_account_number", "beneficiary_bank", "bill_type",
                              "beneficiary_phone_number", "mobile_network", "recepient_phone_number",
                              "recepient_bank_name", "recepient_account_number", "sender_bank_name", "sender"]
        elif action == "transfer":
            exclude_fields = ["user", "account", "transaction_type", "bill_type", "mobile_network", "recepient_phone_number",
                              "recepient_bank_name", "recepient_account_number", "sender_bank_name", "sender"]  # Keep transfer-specific fields
        elif action == "withdraw":
            exclude_fields = ["user", "account", "transaction_type","beneficiary_account_number", "beneficiary_bank", "bill_type",
                              "beneficiary_phone_number", "mobile_network", "recepient_phone_number",
                              "recepient_bank_name", "recepient_account_number", "sender_bank_name", "sender"]
        # Initialize form with POST data, excluding fields as necessary
        trans_form = Transaction_form(request.POST)
        for field in exclude_fields:
            if field in trans_form.fields:
                del trans_form.fields[field]
        
        
        
        try:
            user_info = Account_table.objects.all().get(account_id = accId)
    #         print(user_info.account_type)
           
        except Exception as e:
            messages.error(request, (f'Account verification fails: {e}'))
            return HttpResponsePermanentRedirect(reverse("transaction", args=(accId, action)))

        if trans_form.is_valid():
            tran_list = {}
            
            
            print("form is valid")
            if action == "deposit":
                tran_list["amount"] = trans_form.cleaned_data["transaction_amount"]
                tran_list["transaction_type"] = "deposit"
                print(tran_list)
                # tran_list.update(amount=trans_form.cleaned_data["transaction_amount"])
                # tran_list.update(transaction_type="deposit")
                # print(tran_list)
                tran_list_json = json.dumps(tran_list)
                print(tran_list_json)
            elif action == "transfer":
                tran_list["benef_bank"] = trans_form.cleaned_data["beneficiary_bank"]
                tran_list["benef_acct"] = trans_form.cleaned_data["beneficiary_account_number"]
                tran_list["amount"] = trans_form.cleaned_data["transaction_amount"]
                tran_list["transaction_type"] = "Transfer"
                tran_list_json = json.dumps(tran_list)
            elif action == "withdraw":
                tran_list["amount"] = trans_form.cleaned_data["transaction_amount"]
                tran_list["transaction_type"] = "Withdraw"
                tran_list_json = json.dumps(tran_list)
            
            trans_time = timezone.now()
            return render(request, "transactionapp/confirm.page.html", {"tran_list_json": tran_list_json, "user_info": user_info, "trans_time": trans_time})
            
           
        else: 
            print("Form errors:", trans_form.errors)
            messages.error(request, "Form validation failed.")
            return HttpResponsePermanentRedirect(reverse("transaction", args=(accId, action)))
    else:
        exclude_fields = []
        
        if action == "transfer":
            exclude_fields = ["bill_type", "mobile_network", "sender_bank_name", "sender"]
        elif action == "pay_bill":
            exclude_fields = ["mobile_network", "sender_bank_name", "sender"]
        elif action == "recharge":
            exclude_fields = ["bill_type", "beneficiary_account_number", "sender"]
        else:  # For deposit, exclude everything but amount
            exclude_fields = ["beneficiary_bank", "beneficiary_account_number", "bill_type", "mobile_network", "sender"]
        
        trans_form = Transaction_form(exclude=exclude_fields)
        user_info = Account_table.objects.get(account_id=accId)
        return render(request, 'transactionapp/transaction_form.html', {
            "trans_form": trans_form, "action": action, "user_info": user_info
        })
      
@login_required
def submitTransaction(request, tran_list_json, accId):
    tran_list_json = json.loads(unquote(tran_list_json))
    
    print(tran_list_json)
    with transaction.atomic():
        try:
            balance = Account_table.objects.get(account_id = accId).account_balance
        except Exception as e:
            messages.error(request, (f"Transaction fail to process account balance: {e}"))
            return HttpResponsePermanentRedirect(reverse("transaction", args=(accId, tran_list_json.get("transaction_type"))))
            
        if tran_list_json.get("transaction_type") == "deposit":
            Account_table.objects.filter(user_id = request.user.id, account_id = accId).update(
                account_balance = F("account_balance") + int(tran_list_json.get("amount")))
            transact = Transaction_table(user_id = request.user.id, account_id = accId,
            transaction_amount = tran_list_json.get("amount"), transaction_type = tran_list_json.get("transaction_type"))
        elif tran_list_json.get("transaction_type") == "Transfer":
            if balance < tran_list_json.get("amount"):
                
                messages.error(request, (f"Transaction Fail to process: Insufficient Balance"))
                return HttpResponsePermanentRedirect(reverse("transaction", args=( accId, tran_list_json.get("transaction_type"))))
            else:
                Account_table.objects.filter(user_id = request.user.id, account_id = accId).update(
                    account_balance = F("account_balance") - int(tran_list_json.get("amount")))
                transact = Transaction_table(user_id = request.user.id, account_id = accId,
                transaction_amount = tran_list_json.get("amount"), transaction_type = tran_list_json.get("transaction_type"),
                beneficiary_account_number = tran_list_json.get("benef_acct"), beneficiary_bank = tran_list_json.get("benef_bank"))
            
        elif tran_list_json.get("transaction_type") == "Withdraw":
            if balance < tran_list_json.get("amount"):
                messages.error(request, (f"Transaction Fail to process: Insufficient Balance"))
                return HttpResponsePermanentRedirect(reverse("transaction", args=(accId, tran_list_json.get("transaction_type"))))
            else:
                Account_table.objects.filter(user_id = request.user.id, account_id = accId).update(
                    account_balance = F("account_balance") - int(tran_list_json.get("amount")))
                transact = Transaction_table(user_id = request.user.id, account_id = accId,
                transaction_amount = tran_list_json.get("amount"), transaction_type = tran_list_json.get("transaction_type"),
                
                    
                )
            
        try:
            transact.save()
        except Exception as e:
            messages.error(request, (f'Transaction fail to process: {e}'))
            return HttpResponsePermanentRedirect(reverse("transaction", args=(accId, tran_list_json.get("transaction_type"))))
        
        
    last_transaction = Transaction_table.objects.all().filter(account_id= accId).order_by('-transaction_id').first()
    print(last_transaction)
    if last_transaction:
        messages.success(request, ("Your transaction was successful"))
        return render(request, "transactionapp/receipt_page.html", {"transaction": [last_transaction]})
    else:
        messages.error(request, "No transaction found.")
    return HttpResponseRedirect(reverse("transaction", args=(accId, "deposit"))) 
                
@login_required
def transaction_history(request, userId):
    if request.method == "POST":
        history_form = Transaction_historyForm(request.POST)
        if history_form.is_valid():
            start = history_form.cleaned_data["start_date"]
            end = history_form.cleaned_data["end_date"]
            try:
                tran_history= Transaction_table.objects.all().filter(userId = userId)
                transaction_date_range = [start, end]
                return render(request, "transactionapp/transaction_history.html", {"transaction_history":tran_history})
            except Exception as e:
                messages.error(request, (f"Fail to process request: {e}"))
                return HttpResponsePermanentRedirect(reverse("transaction_history", args=(userId)))
            
        else:
            messages.error(request, (f"Form not filled correctl: {e}"))
            return HttpResponsePermanentRedirect(reverse("transaction_history", args=(userId,)))
    else:
        history_form = Transaction_historyForm
        return render(request, "transactionapp/pin_auth_form.html", {"pin_form": history_form})
       