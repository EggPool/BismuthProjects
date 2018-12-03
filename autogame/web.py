import classes
import tornado.ioloop
import tornado.web
import json

class GetGameByIdHandler(tornado.web.RequestHandler):


    def get(self, hash):
        filename = (f"static/{hash}.json")
        with open (filename) as file:
            text = json.loads(file.read())

            display = ""
            for key, value in text.items():
                display += "<p>"
                display += value
                display += "</p>"

        with open("static/html1") as file:
            self.write(file.read())

        self.write(display)

        self.write("<style>")
        with open("static/style.css") as file:
            self.write(file.read())

        for key, value in text.items():
            self.write("\n")
            self.write("p:nth-child("+str(key)+"){white-space:nowrap;overflow:hidden;opacity:0;animation: type 1s steps(40, end);animation: type2 1s steps(40, end);animation-fill-mode: forwards;animation-delay: "+str(int(key)*2)+"s;}")
            self.write("\n")
        self.write("</style>")

        with open("static/html2") as file:
            self.write(file.read())



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.db = classes.ScoreDb()

        self.db.c.execute("SELECT * FROM scores ORDER BY experience DESC LIMIT 1")
        self.top = self.db.c.fetchone()

        self.write('<title>Autogame</title>\n')

        # html.append('<link rel="stylesheet" type="text/css" href="static/style.css">')
        self.write('<link rel = "icon" href = "static/explorer.ico" type = "image/x-icon" / >\n')
        self.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >')

        self.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')
        self.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script >')



        self.write("<h1>Top Player:</h1>")
        self.write("<table class='table table-responsive'>")
        self.write("<tr>")
        self.write("<th>Start block</th>")
        self.write("<th>Game hash</th>")
        self.write("<th>Game seed</th>")
        self.write("<th>Hero experience</th>")
        self.write("<th>Corpse inventory</th>")
        self.write("</tr>")

        self.write("<tr>")
        self.write(f"<td>{self.top[0]}")
        self.write(f"<td><a href='/hash/{self.top[1]}'>{self.top[1]}</a>")
        self.write(f"<td>{self.top[2]}")
        self.write(f"<td>{self.top[3]}")
        self.write(f"<td>{self.top[4]}")
        self.write("</td></tr>")

        self.write("</table>")


        self.db.c.execute("SELECT * FROM scores")
        self.all = self.db.c.fetchall()
        self.write("<h1>Finished Games:</h1>")

        self.write("<table class='table table-responsive'>")
        self.write("<tr>")
        self.write("<th>Start block</th>")
        self.write("<th>Game hash</th>")
        self.write("<th>Game seed</th>")
        self.write("<th>Hero experience</th>")
        self.write("<th>Corpse inventory</th>")
        self.write("</tr>")

        for line in self.all:
            self.write("<tr>")
            self.write(f"<td>{line[0]}")
            self.write(f"<td><a href='/hash/{line[1]}'>{line[1]}</a>")
            self.write(f"<td>{line[2]}")
            self.write(f"<td>{line[3]}")
            self.write(f"<td>{line[4]}")
            self.write("</td></tr>")

        self.write("</table>")


def make_app():

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        (r"/hash/(.*)", GetGameByIdHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(6060)
    tornado.ioloop.IOLoop.current().start()