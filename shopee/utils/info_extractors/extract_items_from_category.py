class ExtractItemsFromCategory:
  def __init__(self, item):
    self.item = item
  
  def extract(self):
    item_id = self.item.get("itemid")
    shop_id = self.item.get("shopid")
    
    return {
      "itemid": item_id,
      "shopid": shop_id,
    }
    
