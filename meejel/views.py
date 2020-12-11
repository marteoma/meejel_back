import logging

from django.db.utils import IntegrityError
from rest_framework import pagination, status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
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


@api_view(['POST'])
@permission_classes([])
def sign(request, *args, **kwargs):
    try:
        username = request.data['username']
        password = request.data['password']
        User.objects.create(username=username, password=password)
        return Response({"error": "Success"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer

    # pagination_class = PaginationStandard

    def get_queryset(self):
        return self.request.user.instruments.all()

    def destroy(self: Instrument, request, *args, **kwargs):
        self.principles.all().delete()
        return Response({'error': 'Principios borrados'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        old_instrument = Instrument.objects.get(pk=kwargs.get('pk'))
        request.data['category'] = Category.objects.get(name=request.data['category']).pk
        old_instrument.components.all().delete()
        try:
            goals = request.data['Objetivos']
        except KeyError:
            goals = []
        try:
            rules = request.data['Reglas']
        except KeyError:
            rules = []
        try:
            roles = request.data['Roles']
        except KeyError:
            roles = []
        try:
            steps = request.data['Pasos']
        except KeyError:
            steps = []
        try:
            materials = request.data['Materiales']
        except KeyError:
            materials = []
        for i in goals:
            Component.objects.create(component_type='Objetivos', description=i['Oname'], instrument=old_instrument)
        for i in rules:
            Component.objects.create(component_type='Reglas', description=i['Rname'], instrument=old_instrument)
        for i in roles:
            Component.objects.create(component_type='Roles', description=i['Roname'], instrument=old_instrument)
        for i in steps:
            Component.objects.create(component_type='Pasos', description=i['Sname'], instrument=old_instrument)
        for i in materials:
            Component.objects.create(component_type='Materiales', description=i['Maname'], instrument=old_instrument)
        return super(InstrumentViewSet, self).update(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({'error': 'you are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            name = request.data['name']
        except KeyError:
            return Response({'error': 'missing name'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            goals = request.data['Objetivos']
        except KeyError:
            goals = []
        try:
            rules = request.data['Reglas']
        except KeyError:
            rules = []
        try:
            roles = request.data['Roles']
        except KeyError:
            roles = []
        try:
            steps = request.data['Pasos']
        except KeyError:
            steps = []
        try:
            materials = request.data['Materiales']
        except KeyError:
            materials = []
        try:
            new_instrument = Instrument.objects.create(name=name, owner=request.user,
                                                       description=request.data['description'],
                                                       associated_concepts=request.data['associated_concepts'],
                                                       difficulty=request.data['difficulty'], time=request.data['time'],
                                                       groups=request.data['groups'],
                                                       winner_selection=request.data['winner_selection'],
                                                       category=Category.objects.get(name=request.data['category']),
                                                       purpose_reinforce=request.data['purpose_reinforce'],
                                                       purpose_check=request.data['purpose_check'],
                                                       purpose_social=request.data['purpose_social'],
                                                       purpose_teaching=request.data['purpose_teaching'],
                                                       attachments=request.data['attachments'],
                                                       public=request.data['public'])
            for i in goals:
                Component.objects.create(component_type='Objetivos', description=i['Oname'], instrument=new_instrument)
            for i in rules:
                Component.objects.create(component_type='Reglas', description=i['Rname'], instrument=new_instrument)
            for i in roles:
                Component.objects.create(component_type='Roles', description=i['Roname'], instrument=new_instrument)
            for i in steps:
                Component.objects.create(component_type='Pasos', description=i['Sname'], instrument=new_instrument)
            for i in materials:
                Component.objects.create(component_type='Materiales', description=i['Maname'],
                                         instrument=new_instrument)
            return Response({'ok': 'created'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'an instrument with that name already exists'}, status=status.HTTP_409_CONFLICT)


class PrincipleViewSet(viewsets.ModelViewSet):
    serializer_class = PrincipleSerializer

    def get_queryset(self):
        instrument_id = self.kwargs['instrument_pk']
        queryset = Principle.objects.filter(instrument_id=instrument_id)
        return queryset

    def create(self, request, *args, **kwargs):
        instrument_id = self.kwargs['instrument_pk']
        new_principle = Principle.objects.create(principle=request.data['principle'], grade=request.data['grade'],
                                                 instrument_id=instrument_id)
        return Response(self.serializer_class(new_principle).data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class EvidenceViewSet(viewsets.ModelViewSet):
    serializer_class = EvidenceSerializer

    def get_queryset(self):
        instrument = self.kwargs['instrument_pk']
        queryset = Evidence.objects.filter(principle__instrument=instrument)
        return queryset

    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({'error': 'you are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            instrument = Instrument.objects.get(pk=request.data['instrument_id'])
            principles = request.data['Principios']
        except KeyError:
            return Response({'error': 'missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instrument.principles.all().delete()
            for i in principles:
                principle = i['id']
                evidences = i['evidencias']
                level = i['nivel']
                new_principle = Principle.objects.create(instrument=instrument, grade=level, principle=principle)
                for j in evidences:
                    component = Component.objects.get(pk=j)
                    Evidence.objects.create(principle=new_principle, component=component)
            return Response({'ok': 'created'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'algo falló, contacte al administrador'}, status=status.HTTP_409_CONFLICT)
