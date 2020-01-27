from pymongo import ReturnDocument


class GenericDAO:

    @classmethod
    def create_indexes(cls, db):
        # Subclass responsibility
        pass

    @classmethod
    async def get_first(cls, query, projection_dict=None):
        """
        Get first entry matching the given query.
            :returns Full document
        """
        return await cls.collection().find_one(query, projection_dict)

    @classmethod
    async def get_all(cls, query=None, projection_dict=None):
        """
        Get all entries matching the given query. If there is no query, full collection is returned.
            :returns List of full documents
        """
        cursor = cls.collection().find({} if query is None else query, projection_dict)
        documents = []
        while await cursor.fetch_next:
            documents.append(cursor.next_object())
        return documents

    @classmethod
    async def insert(cls, element):
        """
        Insert given element into collection.
            :returns An instance of InsertOneResult (ior.inserted_id gives the created id)
        """
        return await cls.collection().insert_one(element)

    @classmethod
    async def upsert(cls, query, update_dict):
        """
        Creates entry if it doesn't exists and updates it if it does.
            :returns Updated document
        """
        return await cls.collection().find_one_and_update(filter=query,
                                                          update=update_dict,
                                                          upsert=True,
                                                          return_document=ReturnDocument.AFTER)

    @classmethod
    async def update_first(cls, query, updated_fields_dict):
        """
        Update first entry matching given query with the given dictionary.
            :returns Updated document
        """
        return await cls.collection().find_one_and_update(filter=query,
                                                          update={'$set': updated_fields_dict},
                                                          return_document=ReturnDocument.AFTER)

    @classmethod
    def collection(cls):
        # Subclass responsibility
        pass
