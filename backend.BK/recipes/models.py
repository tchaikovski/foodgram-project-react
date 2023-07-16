from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название продуктов')
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единицы измерения',
        help_text='Введите единицы измерения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название тега')
    color = ColorField(
        format='hex',
        verbose_name='Цвет',
        help_text='Введите цвет тега')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Текстовый идентификатор тега',
        help_text='Введите текстовый идентификатор тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):

        return self.slug


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Выберите автора рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/',
        help_text='Выберите изображение рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описания рецепта')

    cooking_time = models.IntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Время приготовления',
        help_text='Введите время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тег рецепта',
        help_text='Выберите тег рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Продукты в рецепте',
        help_text='Выберите продукты рецепта')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Добавить дату создания')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):

        return self.name


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя',
        related_name='purchases'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты',
        help_text='Выберите рецепты для добавления в корзины'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = (
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_cart'),
        )

    def __str__(self):

        return f'{self.user} {self.recipe}'


class IngredientRecipe(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Продукты рецепта',
        help_text='Добавить продукты рецепта в корзину')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    amount = models.IntegerField(
        default=1,
        validators=(MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        ),
        verbose_name='Количество продукта',
        help_text='Введите количество продукта'
    )

    class Meta:
        verbose_name = 'Продукты в рецепте'
        verbose_name_plural = 'Продукты в рецепте'
        constraints = (
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_ingredientrecipe'),
        )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Выберите теги рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(fields=('tag', 'recipe'),
                                    name='unique_tagrecipe'),
        )

    def __str__(self):

        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_favorite'),
        )

    def __str__(self):

        return f'{self.recipe} {self.user}'
