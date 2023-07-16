from http import HTTPStatus

from api.download_cart import DownloadCartView
from api.filters import IngredientSearchFilter, RecipeFilters
from api.serializers import (CartSerializer, FavoriteSerializer,
                             IngredientSerializer, RecipeSerializer,
                             RecipeSerializerPost, RegistrationSerializer,
                             SubscriptionSerializer, TagSerializer)
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from users.models import Subscribe, User


class CreateUserView(UserViewSet):

    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.all()


class SubscribeViewSet(viewsets.ModelViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):

        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = RecipeFilters
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipeSerializerPost


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientSearchFilter)
    pagination_class = None
    search_fields = ('^name',)


class BaseFavoriteCartViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class CartViewSet(BaseFavoriteCartViewSet):

    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    model = Cart


class FavoriteViewSet(BaseFavoriteCartViewSet):

    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite


class DownloadCart(DownloadCartView):

    permission_classes = (permissions.IsAuthenticated,)
