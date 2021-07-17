from typing import List

from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.models import UserOutGet, Users, UserOutPost, ProductOutPost, ProductOutGet, ProductIn, Products, CategoryIn, \
    Categories, CategoryOutGet

router = APIRouter()


@router.get("", response_model=List[UserOutGet], responses={404: {"model": HTTPNotFoundError}})
async def list_users() -> List[UserOutGet]:
    """
    Get users list.
    :return: list users
    """
    return await UserOutGet.from_queryset(Users.all())


@router.get("/{user_id}", response_model=UserOutGet, responses={404: {"model": HTTPNotFoundError}})
async def get_user(user_id: int) -> UserOutGet:
    """
    Get user by id.
    :param user_id: User ID
    :return: User object
    """
    return await UserOutGet.from_queryset_single(Users.get(id=user_id))


@router.post("", response_model=UserOutPost)
async def create_user(username: str, password: str) -> UserOutPost:
    """
    Create new user.
    :param password: plain text password
    :param username: name
    :return: new user object
    """
    user_obj = await Users.create(username=username)
    await user_obj.generate_hashed_password(password)
    return await UserOutPost.from_tortoise_orm(user_obj)


@router.put("/{user_id}", response_model=UserOutGet, responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, username: str, password: str) -> UserOutGet:
    """
    Update user by ID
    :param password: user plain text password
    :param username: user name
    :param user_id: user ID
    :return: updated user object
    """
    user = await Users.filter(id=user_id).first()
    await user.generate_hashed_password(password)
    user.username = username
    await user.save()
    return await UserOutGet.from_queryset_single(Users.get(id=user_id))


@router.get("/{user_id}/products", response_model=List[ProductOutGet], responses={404: {"model": HTTPNotFoundError}})
async def get_user_products(user_id: int) -> List[ProductOutGet]:
    """
    Get all products for user.
    :param user_id: user ID
    :return: list of products
    """
    return await ProductOutGet.from_queryset(Products.filter(owner_id=user_id).all())


@router.get(
    "/{user_id}/product/{product_id}",
    response_model=ProductOutGet,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_user_product_by_product_id(user_id: int, product_id: int) -> ProductOutGet:
    """
    Get product for user by product id.
    :param user_id: user ID
    :param product_id: product ID
    :return: product object
    """
    return await ProductOutGet.from_queryset_single(Products.get(owner_id=user_id, id=product_id))


@router.post("/{user_id}/product/", response_model=ProductOutPost)
async def create_product_for_user(user_id: int, product: ProductIn, categories: List[CategoryIn]) -> ProductOutPost:
    """
    Create product for user
    :param categories: Categories data
    :param user_id: User ID
    :param product: Product data
    :return: new Product
    """
    product_obj = await Products.create(**product.dict(exclude_unset=True))
    product_obj.owner_id = user_id
    for category in categories:
        category_obj = await CategoryOutGet.from_queryset_single(Categories.get(id=category.id))
        await product_obj.categories.add(*category_obj)
    await product_obj.save()
    return ProductOutPost.from_tortoise_orm(product_obj)


@router.put(
    "/{user_id}/product/{product_id}",
    response_model=ProductOutGet,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_product_by_user(user_id: int, product_id: int, product: ProductIn) -> ProductOutGet:
    """
    Full update product for user.
    :param user_id: User ID
    :param product_id: Product id
    :param product: update Product
    :return:
    """
    await Products.filter(id=product_id, owner_id=user_id).update(**product.dict(exclude_unset=True))
    return await ProductOutGet.from_queryset_single(Products.get(id=product_id, owner_id=user_id))


@router.patch("/{user_id}/product/{product_id}")
async def patch_product_for_user(user_id: int, product_id: int, product: ProductIn) -> ProductOutGet:
    """
    Patch product object.
    :param user_id: User ID
    :param product_id: Product ID
    :param product: Product data
    :return: patched product
    """
    old_product = await Products.get(id=product_id, owner_id=user_id)
    await old_product.update_from_dict(product.dict(exclude_unset=True))
    return old_product
