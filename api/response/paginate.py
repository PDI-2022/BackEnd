class Pagination:
    def __init__(self, page, total_pages, items) -> None:
        self.page = page
        self.total_pages = total_pages
        self.items = items

    def serialize(self) -> dict:
        items = list()
        for item in self.items:
            print(item)
            items.append(item.serialize())
        return {"page": self.page, "totalPages": self.total_pages, "result" : items}