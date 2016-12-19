#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from Conversation.conversation import entry
import json

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://postgres:postgres@localhost/columbiaconnect"

engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
    print "Database connected"
    print g.conn
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  return render_template("index.html")

@app.route('/search',methods=['GET'])
def search():
    intent_map = {"get_location":"Get location","location_lecture":"Get location of lecture", "location_office_hours":"Get location of office hours",\
    "get_time":"Get timing","time_lecture":"Get timing of lecture", "time_office_hours":"Get timing of office hours",\
    "reviews":"Get reviews", "suggest_course":"Get suggestion for interests","goodbye":"goodbye","hello":"hello"}
    text = str(request.args["query"])
    response = entry(text)
    if response["found"] == True:
        page = response["page"]
        alt_intents = response["response"]["intents"][1:]
        score = response["response"]["intents"][0]["confidence"]
        for i,a in enumerate(alt_intents):
            alt_intents[i]["intent"] = intent_map[a["intent"]]
        page_new = intent_map[page]

        if page == "hello":
            message = [
            "What are the office hours for professor X?",
            "What are the office hours for course Y?",
            "Review for professor X?",
            "Review for course Y?",
            "Where does professor X sit?",
            "Where is course Y held?",
            "Can you suggest some course for \"keyword\"? (e.g. Database, ML) ",
            "Tell me something about course Y?"
            ]

            context = dict(data=message)
            return render_template("hello.html", **context)

        elif page == "reviews":
            # intent = "location"
            # alt_intents = response["response"]["intents"][1:]
            # alt_intents = [{"confidence":0.004, "intent" : "get_location"},{"confidence":0.2, "intent" : "get_course"}]

            value = response["value"]

            entity = response["response"]["entities"]
            total =0
            positive = 0
            for review in value:
                total += 1
                if review["sentiment"] == "\"positive\"":
                    positive += 1

            pos_percent = format(((positive/float(total)) * 100),'.2f')
            neg_percent = format(100 - ((positive/float(total)) * 100),'.2f')

            total =0
            approving = 0
            disapproving = 0
            neutral = 0
            vindictive = 0
            for review in value:
                total += 1
                if review["tone"] == "Approving":
                    approving += 1
                elif review["tone"] == "Disapproving":
                    disapproving += 1
                elif review["tone"] == "Vindictive":
                    vindictive += 1
                elif review["tone"] == "Neutral":
                    neutral += 1


            app_percent = format(((approving/float(total)) * 100),'.2f')
            dis_percent = format(((disapproving/float(total)) * 100),'.2f')
            vin_percent = format(((vindictive/float(total)) * 100),'.2f')
            neutral_percent = format(((neutral/float(total)) * 100),'.2f')

            context = dict(data=alt_intents, data1=value, data2=pos_percent, data3=neg_percent, data4=entity, data5=[app_percent, dis_percent, vin_percent, neutral_percent],text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            print json.dumps(context, indent=2)
            return render_template(render_file, **context)
        elif page == "location_office_hours":
            value = response["value"]

            for val in value:
                val["timing"] = val["timing"].decode("utf-8")
                print str(val["building"])
                val["location"] = str(val["building"]).replace(' ', '+').replace('&', 'and')
                print str(val["location"])
                val["src"] = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDK0K9X-rKtBwacjisV8vFPTuJBNoM8wFs&q=" + str(val["location"]) + "+of+Columbia+University"
            # alt_intents = response["response"]["intents"][1:]

            entity = response["response"]["entities"]
            context = dict(data=alt_intents, data1=value, data2=entity,text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            return render_template(render_file, **context)

        elif page == "location_lecture":
            value = response["value"]

            for val in value:
                val["timing"] = val["timing"].decode("utf-8")
                print str(val["building"])
                val["location"] = str(val["building"]).replace(' ', '+').replace('&', 'and')
                print str(val["location"])
                val["src"] = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDK0K9X-rKtBwacjisV8vFPTuJBNoM8wFs&q=" + str(val["location"]) + "+of+Columbia+University"
            # alt_intents = response["response"]["intents"][1:]

            entity = response["response"]["entities"]
            context = dict(data=alt_intents, data1=value, data2=entity,text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            return render_template(render_file, **context)

        elif page == "time_office_hours":
            value = response["value"]

            for val in value:
                val["time"] = val["time"].decode("utf-8")
                print str(val["building"])
                val["location"] = str(val["building"]).replace(' ', '+').replace('&', 'and')
                print str(val["location"])
                val["src"] = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDK0K9X-rKtBwacjisV8vFPTuJBNoM8wFs&q=" + str(val["location"]) + "+of+Columbia+University"
            # alt_intents = response["response"]["intents"][1:]

            entity = response["response"]["entities"]
            context = dict(data=alt_intents, data1=value, data2=entity,text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            return render_template(render_file, **context)

        elif page == "time_lecture":
            value = response["value"]

            for val in value:
                val["time"] = val["time"].decode("utf-8")
                print str(val["building"])
                val["location"] = str(val["building"]).replace(' ', '+').replace('&', 'and')
                print str(val["location"])
                val["src"] = "https://www.google.com/maps/embed/v1/place?key=AIzaSyDK0K9X-rKtBwacjisV8vFPTuJBNoM8wFs&q=" + str(val["location"]) + "+of+Columbia+University"
            # alt_intents = response["response"]["intents"][1:]

            entity = response["response"]["entities"]
            context = dict(data=alt_intents, data1=value, data2=entity,text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            return render_template(render_file, **context)

        elif page == "suggest_course":
            value = response["value"]

            # alt_intents = response["response"]["intents"][1:]

            entity = response["response"]["entities"]
            context = dict(data=alt_intents, data1=value, data2=entity,text=text,intent=page_new,score=score)
            render_file = str(page) + ".html"
            return render_template(render_file, **context)

    else:
        intent = response["response"]["intents"][0]
        alt_intents = response["response"]["intents"][1:]
        for i,a in enumerate(alt_intents):
            alt_intents[i]["intent"] = intent_map[a["intent"]]
        intent["intent"] = intent_map[intent["intent"]]
        context = dict(data=alt_intents, intent=intent, text=text)
        return render_template("error.html", **context)


@app.route('/feedback',methods=['GET'])
def feedback():
    message = "Thank you for your feedback. We will incorporate this into our system model to account for the mistake"
    context = dict(data = message)
    #
    # render_template looks in the templates/ folder for files.
    # for example, the below file reads template/index.html
    #
    return render_template("feedback.html", **context)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8080, type=int)
  def run(debug, threaded, host, port):

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=int(os.getenv('VCAP_APP_PORT', 8080)), debug=debug, threaded=threaded)


  run()
