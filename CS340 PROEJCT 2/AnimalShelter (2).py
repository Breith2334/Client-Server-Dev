# Python Testing Script

#TODO: import for your CRUD module

#TODO: Instantiate an instance of your class

#TODO: Use your create function create a new record in the aac database

#TODO: Use your read funtion to return records from the aac database


from pymongo import MongoClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class AnimalShelter(object):
    """
    A class to manage CRUD operations on the AAC animal shelter MongoDB database.
    
    Attributes:
        client: MongoDB client connection
        database: Reference to the 'aac' database
        collection: Reference to the 'animals' collection
    """
    def __init__(self, username='aacuser', password='HarperRoxy2026!!', host='127.0.0.1', port=27017, DB='aac', COL='animals'):
        """
        Initialize the AnimalShelter object and establish MongoDB connection.
        """
        try:
            # Establish connection to MongoDB
            self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/')
            # Access the database
            self.database = self.client[DB]
            # Access the collection
            self.collection = self.database[COL]
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def create(self, data):
        """
        Create a new record in the collection.
        """
        if data:
            try:
                insert_result = self.collection.insert_one(data)
                return insert_result.acknowledged
            except Exception as e:
                logging.error(f"Error inserting document: {e}")
                return False
        else:
            raise ValueError("Nothing to save, because data parameter is empty.")

    def read(self, query):
        """
        Read records from the collection based on the query.
        Accepts an empty dict {} to return all documents.
        """
        if query is not None:        
            try:                     
                documents = self.collection.find(query)
                result = [doc for doc in documents]
                return result
            except Exception as e:
                logging.error(f"Error querying documents: {e}")
                return []
        else:                        
            raise ValueError("Query parameter cannot be None.")

    def update(self, query, updated_data):
        """
        Update documents matching the query.
        """
        if query and updated_data:
            try:
                update_result = self.collection.update_many(query, {"$set": updated_data})
                return update_result.modified_count
            except Exception as e:
                logging.error(f"Error updating documents: {e}")
                return 0
        else:
            raise ValueError("Query or updated_data parameter is empty.")

    def delete(self, query):
        """
        Delete documents matching the query.
        """
        if query:
            try:
                delete_result = self.collection.delete_many(query)
                return delete_result.deleted_count
            except Exception as e:
                logging.error(f"Error deleting documents: {e}")
                return 0
        else:
            raise ValueError("Query parameter is empty.")

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
        logging.info("MongoDB connection closed.")