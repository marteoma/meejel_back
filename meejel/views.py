import logging
import copy

from rest_framework import pagination, status
from rest_framework import viewsets
from rest_framework.response import *

from meejel.serializers import *

log = logging.getLogger("gunicorn")


class PaginationStandard(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'total_pages': self.page.paginator.num_pages
        })


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer
    pagination_class = PaginationStandard

    def get_queryset(self):
        return self.request.user.instruments.all()


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    pagination_class = PaginationStandard

    def get_queryset(self):
        return Assessment.objects.filter(instrument__owner=self.request.user)


class PrincipleViewSet(viewsets.ModelViewSet):
    serializer_class = PrincipleSerializer

    def get_queryset(self):
        assessment_id = self.kwargs['assessment_pk']
        queryset = Principle.objects.filter(assessment_id=assessment_id)
        return queryset

    def create(self, request, *args, **kwargs):
        assessment_id = self.kwargs['assessment_pk']
        new_principle = Principle.objects.create(principle=request.data['principle'], grade=request.data['grade'],
                                                 justification=request.data['justification'], assessment_id=assessment_id)
        return Response(self.serializer_class(new_principle).data, status=status.HTTP_200_OK)


class ComponentViewSet(viewsets.ModelViewSet):
    serializer_class = ComponentSerializer

    def get_queryset(self):
        instrument_id = self.kwargs['instrument_pk']
        queryset = Component.objects.filter(instrument_id=instrument_id)
        return queryset

    def create(self, request, *args, **kwargs):
        instrument_id = self.kwargs['instrument_pk']
        new_component = Component.objects.create(description=request.data['description'], instrument_id=instrument_id,
                                                 component_type=request.data['component_type'])
        return Response(self.serializer_class(new_component).data, status=status.HTTP_200_OK)


class EvidenceViewSet(viewsets.ModelViewSet):
    serializer_class = EvidenceSerializer

    def get_queryset(self):
        assessment = self.kwargs['assessment_pk']
        queryset = Evidence.objects.filter(principle__assessment=assessment)
        return queryset
