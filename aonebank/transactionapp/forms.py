from django import forms
from aonebank.transactionapp.models import Account_table, Transaction_table


class Account_Open_form(forms.ModelForm):
    acc_type = [
        ("", "Select Account Type"),
        ("Savings", "Savings"),
        ("Current", "Current"),
        ("Fixed Deposit", " Fixed Deposit"),
        ("Domicilliary", "Domicilliary"),
        
    ]
    
    
    account_pin = forms.CharField(max_length= 4, help_text="Enter Your 4 Digit Pin")
    account_type = forms.ChoiceField( choices=acc_type)
    
    class Meta:
        model = Account_table
        fields = [
            "account_type",
            "account_pin",
        ]
class changePin_form(forms.Form):
    oldPin = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter your old pin"}), label= "")
    newPin1 = forms.CharField(widget = forms.PasswordInput (attrs={"placeholder": "Enter your new pin"}), label = "")
    newPin2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm new pin"}), label = "")
    

class GeneralParam():
    bank_name = [
        ("", "Select Bank"),
        ("FBN", "FBN"),
        ("FCMB", "FCMB"),
        ("GTB", "GTB"),
        ("UBA", "UBA"),
    ]
    
    bill_type2 = [
        ("", "Select bill type"), 
        ("PHCN", "PHCN"),
        ("GOTV", "GOTV"),
        ("DSTV", "DSTV"),  
    ]
    
    mobile_network2 = [
        ("", "Select mobile network"),
        ("AIRTEL", "AIRTEL"),
        ("ETISALAT", "ETISALAT"),
        ("MTN", "MTN"),
        ("GLO", "GLO"),
    ]
    def get_account(request):
        account_list = [] #("gdhfhhg", "Select your account number")
        account_num = Account_table.objects.all().values()
        # print(account_num)
        for account in account_num:
              account_list.append(account) #(account['account_number'], account['account_number'])
        print(account_list)
        # return account_list


class PinAuthentication_form(forms.Form):
    def __init__(self, *args, **kwargs):
        account_list = kwargs.pop("account_list")
        super().__init__(*args, **kwargs)
        
        self.fields['account_number'] = forms.ChoiceField(
            required= False,
            widget= forms.Select({'class': 'form-control'}), choices = account_list, label=""
        )
        self.fields['pin'] = forms.IntegerField (
            widget= forms.TextInput(attrs={'placeholder': 'Enter your pin', 'class': 'form-contriol'}),
            label = "",
            required= False    
        )
     
class Transaction_form(forms.ModelForm):
    param = GeneralParam()
    beneficiary_account_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Account Number"}), label="", required=False)
    beneficiary_bank = forms.ChoiceField(choices=param.bank_name, label="", required=False)
    bill_type = forms.ChoiceField(choices=param.bill_type2, label="Type of bill", required=False)
    transaction_amount = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Amount"}), label="")
    beneficiary_phone_number = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Beneficiary number"}), label="", required=False)
    mobile_network = forms.ChoiceField(choices=param.mobile_network2, label="Your mobile network", required=False)

    class Meta:
        model = Transaction_table
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)
        
        # Dynamically set fields or exclude fields
        if fields is not None:
            self.fields = {name: self.fields[name] for name in fields if name in self.fields}
        if exclude is not None:
            for field_name in exclude:
                if field_name in self.fields:
                    self.fields.pop(field_name)

        
class Transaction_historyForm(forms.Form):
    start_date = forms.DateField(widget=forms.NumberInput(attrs={"type":"date"}))
    end_date = forms.DateField(widget=forms.NumberInput(attrs={"type": "date"}))