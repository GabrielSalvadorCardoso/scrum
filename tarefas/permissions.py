from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # Permitindo passe livre para ações de leitura
        if request.method in permissions.SAFE_METHODS:
            return True

        # Se o usuario logado é o mesmo do atributo 'criador' do objeto
        # Então permitimos os metodos de escrita
        return obj.criador == request.user