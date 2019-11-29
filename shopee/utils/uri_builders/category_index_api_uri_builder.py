class CategoryIndexApiUriBuilder:
  def __init__(self, *agrs, **kwargs):
    self.kwargs = kwargs
  
  def build_category_index_api_uri(self):
    query_string_elements = ["{0}={1}".format(query_key, query_value) for query_key, query_value in self.kwargs.items()]
    return "?" + "&".join(query_string_elements)
