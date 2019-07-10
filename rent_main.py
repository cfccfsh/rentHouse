from flask import Flask,render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
# from crawl import main
import json




def create_app():
    app = Flask(__name__)
    return app

app = create_app()

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/rentHouse"
#
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
app.config["DEBUG"] = True

app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)

class House(db.Model):
    __tablename__ = "house"
    id = db.Column(db.Integer,primary_key=True)
    houseTitle = db.Column(db.String(120))
    houseLocation = db.Column(db.String(120),nullable=False,index=True)
    houseMoney = db.Column(db.Integer)
    houseUrl = db.Column(db.TEXT(65535))

    def to_dict(self):
        dic = {
            "id":self.id,
            "houseTitle":self.houseTitle,
            "houseLocation":self.houseLocation,
            "houseMoney":self.houseMoney,
            "houseUrl":self.houseUrl,
        }
        return dic

db.create_all()


# @app.route("/add")
# def add():
#     house_list = main()
#     a = 0
#     for item in range(len(house_list)):
#         item = House()
#         item.houseTitle = house_list[a][0].strip()
#         item.houseLocation = house_list[a][1]
#         item.houseMoney = int(house_list[a][2])
#         item.houseUrl = house_list[a][3]
#         db.session.add(item)
#         a += 1
#         # db.session.commit()
#     return "数据插入完成"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/indexServer")
def indexServer():
    houses = House.query.all()
    list_h = []
    for i in houses:
        list_h.append(i.to_dict())
    return json.dumps(list_h)



if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True,host="0.0.0.0",port=80)