from src.database.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.package.package_status import PackageStatus
from src.model.package.status import Status


class PackageDAO(GenericDAO):

    @classmethod
    async def exists(cls, package_id: str) -> bool:
        return await cls.get_first({'_id': package_id}) is not None

    @classmethod
    async def find(cls, package_id: str) -> Status:
        """ Return the last known status of the given package """
        document = await cls.get_first({'_id': package_id})
        # Get instance directly from its name
        return None if not document else getattr(PackageStatus, document['last_status'], None)

    @classmethod
    async def store(cls, package_id: str, last_status: str):
        """ Store new call in database. """
        await cls.upsert({'_id': package_id}, {'$set': {'last_status': last_status}})

    @classmethod
    def collection(cls):
        return Mongo.get().packages
