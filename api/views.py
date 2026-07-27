from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import Company

from django.db import transaction
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import KBEntry, QueryLog

from django.db.models import Count, Sum

from rest_framework.decorators import api_view, permission_classes

from .permissions import IsAdminUser
from .models import QueryLog

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        company = Company.objects.get(user=user)
        company.company_name = request.data.get("company_name")
        company.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "company_name": company.company_name,
                "api_key": company.api_key,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:

        return Response(
            {
                "message": "Invalid username or password"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)
    company = Company.objects.get(user=user)

    return Response(
        {
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "company_name": company.company_name,
            "api_key": company.api_key,
        }
    )


@api_view(["POST"])
def kb_query(request):

    company = request.user.company
    query = request.data.get("query", "").strip()

    if not query:
        return Response(
            {"error": "Query is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():

        kb_entries = KBEntry.objects.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query)
        )

        QueryLog.objects.create(
            company=company,
            search_term=query,
            results_count=kb_entries.count()
        )

    results = []

    for entry in kb_entries:

        results.append(
            {
                "id": entry.id,
                "question": entry.question,
                "answer": entry.answer,
                "category": entry.category,
            }
        )

    return Response(
        {
            "count": len(results),
            "results": results
        }
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def usage_summary(request):

    total_queries = (
        QueryLog.objects.aggregate(
            total=Sum("results_count")
        )["total"] or 0
    )

    active_companies = (
        QueryLog.objects.values("company")
        .distinct()
        .count()
    )

    top_search_terms = (
        QueryLog.objects.values("search_term")
        .annotate(
            count=Count("search_term")
        )
        .order_by("-count")[:5]
    )

    return Response(
        {
            "total_queries": total_queries,
            "active_companies": active_companies,
            "top_search_terms": top_search_terms,
        }
    )