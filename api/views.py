import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Payment, Organization
from .serializers import BankWebhookSerializer, OrganizationBalanceSerializer, OrganizationCreateSerializer

logger = logging.getLogger(__name__)

class OrganizationListCreateView(APIView):
    def get(self, request):
        organizations = Organization.objects
        serializer = OrganizationBalanceSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inn = serializer.validated_data['inn']
        organization, created = Organization.objects.get_or_create(inn=inn)

        if not created:
            return Response(
                {"detail": "Organization already exists."},
                status=status.HTTP_200_OK
            )

        return Response(
            OrganizationBalanceSerializer(organization).data,
            status=status.HTTP_201_CREATED
        )

class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        try:
            organization = Organization.objects.get(inn=inn)
            serializer = OrganizationBalanceSerializer(organization)
            return Response(serializer.data)
        except Organization.DoesNotExist:
            return Response({"detail": "Organization not found"}, status=404)


class BankWebhookView(APIView):
    def post(self, request):
        serializer = BankWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        operation_id = data["operation_id"]
        amount = data["amount"]
        payer_inn = data["payer_inn"]
        document_number = data["document_number"]
        document_date = data["document_date"]

        if Payment.objects.filter(operation_id=operation_id).exists():
            return Response({"detail": "Already processed"}, status=status.HTTP_200_OK)

        payer, created = Organization.objects.get_or_create(inn=payer_inn)
        old_balance = payer.balance
        payer.balance += amount
        payer.save()

        Payment.objects.create(
            operation_id=operation_id,
            amount=amount,
            payer=payer,
            document_number=document_number,
            document_date=document_date,
        )

        logger.info(f"Payer {payer.inn} balance changed from {old_balance} to {payer.balance}")

        return Response({"detail": "Payment processed"}, status=status.HTTP_201_CREATED)
