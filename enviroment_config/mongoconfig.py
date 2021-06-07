import gridfs
from pymongo.mongo_client import MongoClient

###########################
###########################upload demo video to Mongo
storageDB = MongoClient()['Winterstore-Storage']
gridFSConnection = gridfs.GridFS(storageDB)

#put a demo file  
fileToInserted = gridFSConnection.put(open("demo.webm","rb"),filename="demoFile")

#store reference
mongoClient = MongoClient()
db = mongoClient["Winterstore"]
db["Application"].insert_one({
    "owner" : "admin",
    "fileName" : "demo.webm",
    "reference" : fileToInserted,
    "key" : "HUJDKMEBEJN2G456SGTYINGHT6782HBCDHETYUSHJTIONH7890IFHGR678HNGJOTUI"
}) 


print("created demo file")
########################################################################################


#######################
#######################upload getting started pdf
#put a demo file  
fileToInserted = gridFSConnection.put(open("getting-started.pdf","rb"),filename="getting-started")
mongoClient = MongoClient()
db = mongoClient["Winterstore"]
db["Application"].insert_one({
    "owner" : "admin",
    "fileName" : "getting-started.pdf",
    "reference" : fileToInserted,
    "key" : "HYU789IUJ87YHUYT67YGVCFDSER456YTGVBNMKJIKJJ8UUY76TTTFDSER543EFRT"
})


print("created getting started pdf")
########################################################################################
print("done")
