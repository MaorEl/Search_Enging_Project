class TermInfo:
    df = 0
    tf_in_corpus=0

    def add_df (self, number):
        self.df += number

    def get_df (self):
        return self.df

    def add_tf (self, number):
        self.tf_in_corpus += number

    def get_tf (self):
        return self.tf_in_corpus