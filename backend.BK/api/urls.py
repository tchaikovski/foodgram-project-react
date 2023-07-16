from api.views import (CartViewSet, CreateUserView, DownloadCart,
                       FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                       SubscribeViewSet, TagViewSet)
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', CreateUserView, basename='users')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('recipes/download_shopping_cart/',
         DownloadCart.as_view(), name='dowload_shopping_cart'),
    path('users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
    path('', include(v1_router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', views.obtain_auth_token),
]
