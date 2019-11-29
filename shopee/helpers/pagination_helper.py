class PaginationHelper:
  def __init__(self, total, step):
    self.total = total
    self.step = step

  def create_paginatation_list(self):
    ## TODO: Refactor using list comprehension
    num_full_page = self.total // self.step
    result = list()
    for idx in range(num_full_page):
      result.append({
        "limit" : self.step,
        "offset": (self.step * idx),
      })
    result.append({
      "limit": self.total % self.step,
      "offset": (self.step * num_full_page),
    })
    return result


