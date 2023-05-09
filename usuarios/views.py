from rest_framework import viewsets
from usuarios.models import Usuario, Pessoa
from usuarios.serializers import AddUsuarioSerializer, PessoaSerializer
from core.serializers import EnderecoSerializer, TelefoneSerializer
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from core.models import Endereco, Telefone



# class UsuarioViewSet(viewsets.ViewSet):
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return UsuarioAddSerializer
#         else:
#             return UsuarioAddSerializer

#     def get_queryset(self):
#         queryset = Usuario.objects.all()
#         return queryset

#     def get_object(self):
#         queryset = self.get_queryset()
#         pk = self.kwargs.get('pk')
#         obj = get_object_or_404(queryset, pk=pk)
#         return obj        

#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         return serializer_class(*args, **kwargs)            

#     def list(self, request):
#         serializer = self.get_serializer(self.get_queryset(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UsuarioCreateView(ModelViewSet):
    serializer_class = AddUsuarioSerializer
    queryset = Usuario.objects.all()


    def create(self, request, *args, **kwargs):
        print("aqui no usuario create view")
        # print(request.data)
        data = request.data
        endereco_data = request.data['pessoa']['endereco']
        telefone_data = request.data['pessoa']['telefone']


        
        # with transaction.atomic():
        endereco = EnderecoSerializer(data=endereco_data)
        telefone = TelefoneSerializer(data=telefone_data)
        

        endereco.is_valid(raise_exception=True)
        telefone.is_valid(raise_exception=True)

        endereco_obj = endereco.save()
        telefone_obj = telefone.save()

        print("¨"*89)
        print(data.keys())
        print(data['pessoa'].pop('endereco'))
        print(data['pessoa'].pop('endereco'))
        print("¨"*89)





        endereco = Endereco.objects.create(**endereco_data)
        print(endereco)



        
        return super().create(request, *args, **kwargs)    

