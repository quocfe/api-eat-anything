from flask import Flask
from flask_restx import Api, Resource
from models import db, Post
from schemas import PostSchema

app = Flask(__name__)
api = Api(app)

# Config Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db
db.init_app(app)


# Create a simple Post resource
@api.route("/posts")
class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        post_schema = PostSchema(many=True)
        return post_schema.dump(posts)


@api.route("/post/<int:id>")
class PostResource(Resource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        post_schema = PostSchema()
        return post_schema.dump(post)


if __name__ == "__main__":
    app.run(debug=True)
