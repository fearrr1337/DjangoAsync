class ArticlePolicy:
    def __init__(self, user, article):
        self.user = user
        self.article = article

    def can_view(self):
        return True

    def can_edit(self):
        return self.article.author == self.user

    def can_delete(self):
        return self.article.author == self.user

    def can_create(self):
        return self.user.is_authenticated