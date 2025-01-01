from django.urls import path, re_path
from aonebank.transactionapp import views as tran_view


urlpatterns = [
    re_path(r'^new_account/(?P<userId>\d+)/', tran_view.create_newAccount, name = "new_Account"), 
    re_path(r'^my_account/(?P<userId>\d+)/', tran_view.displayMyAccount, name = "my_Account"),
    re_path(r'^change_pin/(?P<accId>\d+)/', tran_view.changePin, name= "change_pin"),
    re_path(r'^reset_pin/(?P<accId>\d+)/(?P<userId>\d+)/', tran_view.resetPin, name = "reset_pin" ),
    re_path(r'^pin_auth/(?P<action>\w+)', tran_view.pinAunthentication, name="pin_auth"),
    re_path(r'^transaction/(?P<accId>\d+)/(?P<action>\w+)', tran_view.userTransaction, name = "transaction"),
    path('submit_transaction/<str:tran_list_json>/<int:accId>/'
         , tran_view.submitTransaction, name="submit_transaction"),
    re_path(r'^transaction_history/(?P<userId>\d+)/', tran_view.transaction_history, name = "transaction_history"),
]
