from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_index = db.Column(db.Integer, nullable=True)
    sparse_vector = db.Column(db.Text)

    def __str__(self):
        return "ID: %s, vector: %s" % (self.id, self.sparse_vector)


class ClusterInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.Integer)
    clusters_count = db.Column(db.Integer)

    def __str__(self):
        return "Cauterization info"