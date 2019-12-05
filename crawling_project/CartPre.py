
import pandas as pd
import json

class CartPre:
    
    def __init__(self):
        self.data1 = pd.read_csv("cartrider/cart.csv")
        self.data2 = pd.read_csv("cartrider/cart1.csv")
        self.df1 = pd.DataFrame(self.data1)
        self.df2 = pd.DataFrame(self.data2)
        self.df = pd.concat([self.df1,self.df2], axis=0, ignore_index=True)
        
    def preprocess(self):
        track_null = list(self.df.loc[self.df["trackId"].isnull()].index)
        self.df = self.df.drop(track_null).reset_index(drop=True)
        column_ununi = list(self.df.loc[self.df["kart"] == "kart"].index)
        self.df = self.df.drop(column_ununi).reset_index(drop=True)
        self.df.loc[self.df["matchRank"] == "99","matchRank"] = "8"
        self.df.loc[self.df["matchRank"] == 99,"matchRank"] = "8"
        self.df.loc[self.df["matchRank"] == "NaN","matchRank"] = "8"
        self.df.loc[self.df["matchRank"].isnull(),"matchRank"] = "8"
        self.df["matchRank"] = self.df["matchRank"].astype("int")
        self.df1 = self.df.groupby("kart").size().reset_index()
        self.df1.sort_values(by = 0,ascending=False)
        self.df1 = self.df1.rename(columns={0:"count"})
        self.df1 = self.df1.loc[self.df1["count"] >= 12,:].reset_index(drop=True)
        kart_sort = list(self.df1["kart"])
        self.df = self.df.loc[self.df["kart"].isin(kart_sort),:].reset_index(drop=True)
        
        return self.df
    
    def pre_decode(self):

        with open("kart.json", "r") as f_kart:
            kart_json = json.load(f_kart)

        with open("track.json", "r") as f_track:
            track_json = json.load(f_track)

        def decode_kart(kart_hash):
            for kart_dict in kart_json:
                if kart_dict["id"] == kart_hash:
                    return kart_dict["name"]
                    break

        def decode_track(track_hash):
            for track_dict in track_json:
                if track_dict["id"] == track_hash:
                    return track_dict["name"]
                    break

        self.df["kart"] = self.df["kart"].apply(decode_kart)
        self.df["trackId"] = self.df["trackId"].apply(decode_track)
        
        return self.df
    
    def pre_groupby(self):
        df_gt = self.df.groupby("trackId").size().reset_index()
        df_gt = df_gt.sort_values(by = 0,ascending=False).reset_index()
        map_top5 = list(df_gt["trackId"][:5])
        df_kt = self.df.groupby("kart").size().reset_index()
        df_kt = df_kt.sort_values(by = 0,ascending=False).reset_index()
        kart_top5 = list(df_kt["kart"][:5])
        df_map = self.df.loc[self.df["trackId"].isin(map_top5),:].reset_index(drop=True)
        df_map = df_map.loc[df_map["kart"].isin(kart_top5),:].reset_index(drop=True)
        df_mapkart = df_map.groupby(["trackId", "kart"]).agg({"matchRank": ["count","mean"]}).reset_index()
        df_mapkart = df_mapkart.sort_values(["trackId", ("matchRank", 'count')], ascending=False)
        df_mapkart = df_mapkart.set_index(['trackId','kart'])
        
        return df_mapkart
