from .models import AccountType, LookupName, PaymentDay, Tax, LookupType
from rest_framework import generics
from rest_framework import permissions
from .serializers import (
    LookupTypeSerializer,
    LookupSerializer,
    TaxSerializer,
    ChartOfAccountTypeSerializer,
    PaymentDaySerializer,
)

# Create your views here.
# ---------------------- Views for Lookups Module ---------------------------------#


class LookupTypeListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupTypeSerializer
    queryset = LookupType.objects.all()


class LookupListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LookupSerializer

    def get_queryset(self):
        return LookupName.objects.filter(lookup_type__lookup_type=self.kwargs['lookup'])


class PayrollTaxListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TaxSerializer

    def get_queryset(self):
        if "payrolltax" == self.kwargs['lookup'].lower():
            return Tax.objects.filter(lookup_name__lookup_name=self.kwargs['lookup'].lower()).values('id', 'irfp')
        return Tax.objects.filter(lookup_name_id=self.kwargs['lookup'])


class ContactTaxListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TaxSerializer

    def get_queryset(self):
        lookup = LookupName.objects.filter(pk=self.kwargs['lookup']).first()
        if lookup:
            if "client" == lookup.lookup_name.lower() or "debitor" == lookup.lookup_name.lower():
                return Tax.objects.filter(lookup_name_id=self.kwargs['lookup']).values('id', 'vat', 'equiv')
            if "provider" == lookup.lookup_name.lower() or "creditor" == lookup.lookup_name.lower():
                return Tax.objects.filter(lookup_name_id=self.kwargs['lookup']).values('id', 'vat', 'ret')
        return Tax.objects.none()


class ChartOfAccountTypeAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ChartOfAccountTypeSerializer

    def get_queryset(self):
        if not LookupName.objects.filter(pk=self.kwargs['lookup']).exists():
            raise LookupName.DoesNotExist
        lookup = LookupName.objects.filter(pk=self.kwargs['lookup']).first()
        if "client" == lookup.lookup_name.lower() or "debitor" == lookup.lookup_name.lower():
            return AccountType.objects.filter(category__lookup_name='Income')
        if "provider" == lookup.lookup_name.lower() or "creditor" == lookup.lookup_name.lower():
            return AccountType.objects.filter(category__lookup_name='Expense')
        return AccountType.objects.none()


class PaymentDayListAPIView(generics.ListAPIView):
    queryset = PaymentDay.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentDaySerializer
