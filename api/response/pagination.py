class Pagination:
    def __init__(self, results, page, offset, total):
        self.results = list()
        for r in results:
            self.results.append(r.serialize())
        self.page = page
        self.offset = offset
        self.total = total
