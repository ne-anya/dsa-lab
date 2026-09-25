import os
from datetime import datetime, timezone

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime(timezone=True), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)


def create_database_url():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")

    required = {
        "DB_HOST": host,
        "DB_PORT": port,
        "DB_USER": user,
        "DB_PASSWORD": password,
        "DB_NAME": name,
    }

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = create_database_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/hello", methods=["GET"])
def hello():
    visit = Visit(
        visited_at=datetime.now(timezone.utc),
        ip_address=request.remote_addr,
    )

    db.session.add(visit)
    db.session.commit()

    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)