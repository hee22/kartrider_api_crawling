import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb server ip")
cartrider = client.cartrider.match
results = cartrider.find()
df = pd.DataFrame(results)
