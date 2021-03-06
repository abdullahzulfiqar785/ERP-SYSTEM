from django.db import models
from Contact.models import Contact
from Core.models import Company
from Lookup.models import Tax, AccountType
# Create your models here.


class Expense(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyExpenses")
    accounting_seat = models.CharField(max_length=12)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='ExpenseContactSeats')
    invoice_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    chart_of_account = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='ExpenseAccounts')


class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="expense_items")
    base_amount = base_amount = models.DecimalField(max_digits=10, decimal_places=2,)
    vat = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="expenseVat")
    calculated_vat = models.DecimalField(max_digits=8, decimal_places=2, )
    ret = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="expenseRet")
    calculated_ret = models.DecimalField(max_digits=8, decimal_places=2,)


class Purchase(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyPurchases")
    accounting_seat = models.CharField(max_length=12)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='PurchaseContactSeats')
    invoice_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    chart_of_account = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='PurchaseAccounts')


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_items")
    base_amount = models.DecimalField(max_digits=10, decimal_places=2,)
    vat = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="purchaseVat")
    calculated_vat = models.DecimalField(max_digits=8, decimal_places=2, )
    ret = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="purchaseRet")
    calculated_ret = models.DecimalField(max_digits=8, decimal_places=2,)


class Asset(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyAssets")
    accounting_seat = models.CharField(max_length=12)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='AssetContactSeats')
    invoice_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    chart_of_account = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name='assetAccounts')


class AssetItem(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="asset_items")
    base_amount = base_amount = models.DecimalField(max_digits=10, decimal_places=2,)
    vat = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="AssetVat")
    calculated_vat = models.DecimalField(max_digits=8, decimal_places=2, )
    ret = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, related_name="AssetRet")
    calculated_ret = models.DecimalField(max_digits=8, decimal_places=2,)
