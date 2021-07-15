from typing import List

from fastapi import APIRouter, Body, Depends
from starlette import status
from tortoise.contrib.fastapi import HTTPNotFoundError

from app.models import CategoryOutGet, Categories, CategoryOutPost, CategoryIn

router = APIRouter()


@router.get("", response_model=List[CategoryOutGet], responses={404: {"model": HTTPNotFoundError}})
async def list_categories() -> List[CategoryOutGet]:
    """
    Get list of all categories.
    :return: list categories
    """
    return await CategoryOutGet.from_queryset(Categories.all())


@router.get("/{category_id}", response_model=CategoryOutGet, responses={404: {"model": HTTPNotFoundError}})
async def get_category(category_id: int) -> CategoryOutGet:
    """
    Get category by id.
    :param category_id: Category ID
    :return: Category object
    """
    return await CategoryOutGet.from_queryset_single(Categories.get(id=category_id))


@router.post("", response_model=CategoryOutPost)
async def create_category(category: CategoryIn) -> CategoryOutPost:
    """
    Create new category.
    :param category: category data
    :return: new category object
    """
    category_obj = await Categories.create(**category.dict(exclude_unset=True))
    return await CategoryOutPost.from_tortoise_orm(category_obj)


@router.put("/{category_id}", response_model=CategoryOutGet, responses={404: {"model": HTTPNotFoundError}})
async def update_category(category_id: int, category: CategoryIn) -> CategoryOutGet:
    """
    Update category by ID.
    :param category: category data
    :param category_id: category ID
    :return:
    """
    await Categories.filter(id=category_id).update(**category.dict(exclude_unset=True))
    return await CategoryOutGet.from_queryset_single(Categories.get(id=category_id))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int) -> dict:
    delete_count = await Categories.filter(id=category_id).delete()
    pass