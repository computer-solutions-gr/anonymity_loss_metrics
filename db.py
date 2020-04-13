# !/usr/bin/env python
# coding=utf-8

import pymongo
#import pprint
#pp = pprint.PrettyPrinter(indent=4)

class MongoRepository:

    def __init__(self, host = "localhost", port = 27017, schema = "etl_test"):
        self.client = pymongo.MongoClient(host,port)
        self.db = self.client[schema]
        # self.db = self.client.etl_test

    def list_all(self, resourceType):
        resource = self.db[resourceType]
        return resource.find({})
    
    def get( self, resourceType, *, key = None, vals = [] ):
        resource = self.db[resourceType]
        field_exclude = "_id"

        if ( (key == None) or (vals == []) or (vals == None) ):
            result = resource.find({}, {field_exclude: False} )
        elif isinstance(vals, list):
            result = resource.find( { key: { "$in" : vals } }, {field_exclude: False} )
        else:
            result = resource.find( { key: vals }, { field_exclude: False } )
        
        return result
    
    def get_one( self, resourceType, *, key = None, vals = [] ):
        resource = self.db[resourceType]
        field_exclude = "_id"

        if ( (key == None) or (vals == []) or (vals == None) ):
            result = resource.find_one({}, {field_exclude: False} )
        elif isinstance(vals, list):
            result = resource.find_one( { key: { "$in" : vals } }, {field_exclude: False} )
        else:
            result = resource.find_one( { key: vals }, {field_exclude: False} )
        
        return result
    
    def insert( self, resourceType, datum ):
        # check if user is unique
        try:
            resource = self.db[resourceType]
            resource.insert(datum)
        except:
            print(f"\nSomething went wrong")
        #db.collection.ensureIndex({"username":1}, {unique:true})
        
    # def group_by( self, resourceType, group_attrs ):

    #     resource = self.db[resourceType]
    #     #build group_fields dict

    #     group_fields = { str(attr): "$" + str(attr) for attr in group_attrs }

    #     result = resource.aggregate([
    #     }   
    #         "$group": {
    #             "_id" : group_fields ,
    #             "count" : { "$sum": 1 }
    #         }
    #     }
    #     ])
    #     return result

    

