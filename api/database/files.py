from api.database.models import UserFile


async def add_file_db(data: UserFile):
    file = UserFile(**data.dict())
    return await file.save()


async def get_all_files():
    return await UserFile.objects.all()


async def get_files_by_id_db(file_id: int):
    return await UserFile.objects.get_or_none(id=file_id)


async def delete_file_db(file_id: int):
    file = await UserFile.objects.get_or_none(id=file_id)
    if file:
        await file.delete()
        return file.id
    return None
