from routes import app
from flask_sqlalchemy import SQLAlchemy

app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://acuvakovxkimbz:902cb12d5d5773faae63f2888c9b66c9eaef90f63f3fbef0a8557bed9ad9ff2f@ec2-35-169-9-79.compute-1.amazonaws.com:5432/d3nnliob7oo57t'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
