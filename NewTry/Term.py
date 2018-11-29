class Term:
    df = 1
    post_file_ptr = None

    def add_df (self, number):
        self.df += number

    def get_df (self):
        return self.df

    def set_ptr(self, ptr):
        self.post_file_ptr = ptr

    def get_ptr(self):
        return self.post_file_ptr
