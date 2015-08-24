class Pagination:
    def __init__(self, total, start = 0, rows = 20, show_pages = 10):
        assert total >= 0
        if rows < 0:
            rows = 20
        if start < 0:
            start = 0
        if show_pages <= 0:
            show_pages = 10
        self.total = total
        self.start = start
        self.rows = rows
        self.current_page = start // rows + 1
        self.current_page_start = start + 1
        self.current_page_end = min(self.current_page_start + rows - 1, total)
        self.max_page = total // rows 
        if not total % rows == 0:
            self.max_page += 1
        self.min_show_page = max(self.current_page - show_pages // 2, 1)
        self.max_show_page = min(self.min_show_page + show_pages, self.max_page)
        self.pages = [(page_id, get_page_start(page_id, rows),) for page_id in range(self.min_show_page, self.max_show_page + 1)]
        if self.current_page > 1:
            self.pre_page = self.current_page - 1
            self.pre_page_start = get_page_start(self.pre_page, rows)     #could be 0
        if self.current_page < self.max_show_page:
            self.next_page = self.current_page + 1
            self.next_page_start = get_page_start(self.next_page, rows)
        
def get_page_start(page_id, rows):
    assert page_id > 0
    return (page_id - 1) * rows