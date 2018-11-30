class TermInfo:
    df = 0
    post_file_ptr = None
    tf_in_corpus=0

    def add_df (self, number):
        self.df += number

    def get_df (self):
        return self.df

    def set_ptr(self, ptr):
        self.post_file_ptr = ptr

    def get_ptr(self):
        return self.post_file_ptr

    def add_tf (self, number):
        self.tf_in_corpus += number

    def get_tf (self):
        return self.tf_in_corpus