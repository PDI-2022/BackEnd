class Pagination:
    def __init__(self, results, page, offset, total):
        self.results = results
        self.page = page
        self.offset = offset
        self.total = total

    def serialize(self) -> dict:
        serialized_results = list()
        for r in self.results:
            serialized_results.append(r.serialize())
        return {
            "page": self.page,
            "offset": self.offset,
            "total": self.total,
            "results": serialized_results,
        }
