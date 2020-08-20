import tornado.ioloop
import tornado.web
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search

ES_INDEX = 'anue-001'
PORT = 8020


class MainHandler(tornado.web.RequestHandler):
    client = Elasticsearch()

    def get(self):
        self.render("index.html", response=None)

    def post(self):
        input_text = self.get_body_argument(name="my_query")

        q = Q("multi_match", query=input_text, fields=['title', 'content'])
        s = Search(using=self.client, index=ES_INDEX).query(q)
        response = s.execute()

        self.render("index.html", response=response)


if __name__ == "__main__":
    try:
        application = tornado.web.Application([
            (r"/anue", MainHandler),
        ])
        application.listen(PORT)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
        print("Server Shutdown!")
        exit(1)
