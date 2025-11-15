
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer  # Cambiado aquí

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superadmin)

class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   (request.user.is_admin or request.user.is_superadmin))

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer  # Cambiado aquí

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrSuperAdmin]
        else:
            permission_classes = [IsAdminOrSuperAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return CustomUser.objects.all()
        elif user.is_admin:
            return CustomUser.objects.filter(is_superadmin=False)
        return CustomUser.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save()
        
        if user.is_superadmin:
            if self.request.data.get('is_admin'):
                instance.is_admin = True
                instance.save()
        else:
            instance.is_superadmin = False
            instance.is_admin = False
            instance.save()

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.save()
        
        if user.is_superadmin:
            if 'is_admin' in self.request.data:
                instance.is_admin = self.request.data['is_admin']
                instance.save()
        else:
            instance.is_superadmin = False
            if 'is_admin' in self.request.data:
                instance.is_admin = False
            instance.save()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperAdmin]

    @action(detail=True, methods=['post'])
    def assign_permissions(self, request, pk=None):
        group = self.get_object()
        permission_ids = request.data.get('permission_ids', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.set(permissions)
        return Response({'status': 'permissions assigned'})

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperAdmin]