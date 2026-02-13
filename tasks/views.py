from rest_framework import viewsets, permissions,generics
from .models import Task,Note
from .serializers import TaskSerializer,NoteSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView






class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def note_list(request):
    if request.method=='GET':
        queryset=Note.objects.filter(user=request.user)
        serialezer=NoteSerializer(queryset,many=True)
        return Response(serialezer.data)
    else:
        serialezer=NoteSerializer(data=request.data)
        if serialezer.is_valid():
            serialezer.save(user=request.user)
            return Response(serialezer.data,status=status.HTTP_201_CREATED)
        return Response(serialezer.errors,status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def note_details(request,pk):
        try:
            note=Note.objects.get(id=pk)
            if note.user != request.user:
              return Response({"error": "Not allowed"}, status=403)

        except Note.DoesNotExist:
            return Response({"error":"note does not exist"},status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            
            serializer=NoteSerializer(note)
            return Response(serializer.data)

        elif request.method in ['PUT' ,'PATCH']:
             serializer = NoteSerializer(note, data=request.data, partial=(request.method=='PATCH'))
             if serializer.is_valid():
                  serializer.save(user=request.user)
                  return Response(serializer.data,status=status.HTTP_200_OK)
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:   
         note.delete()
         return Response({"message":"task delete successfully"},status=status.HTTP_204_NO_CONTENT)
    


@permission_classes([IsAuthenticated])
class NoteListCreateView(APIView):
    def get(self,request):
        notes=Note.objects.filter(user=request.user)
        serializer=NoteSerializer(notes,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
########################################################################################

class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Note.objects.get(id=pk, user=user)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Not found"}, status=404)

        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Not found"}, status=404)

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Not found"}, status=404)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        note = self.get_object(pk, request.user)
        if not note:
            return Response({"error": "Not found"}, status=404)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

  ###########################################################################

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

class NoteListCreateView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin
):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class NoteDetailView(
    GenericAPIView,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def patch(self, request, pk):
        return self.partial_update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
    
######################َ##ModelViewSet:


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#############################################################3

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotePagination

    # Filters
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Filtering
    filterset_fields = ['title']

    # Search
    search_fields = ['title', 'content']

    # Ordering
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # default

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
