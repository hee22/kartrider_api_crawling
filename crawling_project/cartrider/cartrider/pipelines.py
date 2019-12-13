from .mongodb import collection

class CartriderPipeline(object):
    
    def process_item(self, item, spider):
        
        data = { "matches": item["matches"], 
                 "trackId": item["trackId"],
                 "kart": item["kart"], 
                 "matchRank": item["matchRank"],
                 "rankinggrade2": item["rankinggrade2"],
               }
        
        collection.insert(data)
        
        return item
