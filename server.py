#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://vs2567:5769@w4111vm.eastus.cloudapp.azure.com/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
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

  # DEBUG: this is debugging code to see what request looks like

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/clubInterestingQuery',methods=['GET'])
def clubInterestingQuery():
  print request.args
  clubid = str(request.args['club_id'])
  print clubid
  print '1'
  players = g.conn.execute('SELECT P.fname, P.lname, (SELECT count(*) AS total_titles FROM "Club_Title_Record" R WHERE C.clubid = R.clubid GROUP BY clubid) FROM \"Owner\" O, \"Club_Owner\" C, \"Person\" P WHERE C.clubid = (SELECT A.clubid AS clubid FROM (SELECT clubid, count(*) AS COUNT FROM \"Club_Title_Record\" GROUP BY clubid)A WHERE A.COUNT >= ALL (SELECT COUNT(*) AS COUNT FROM \"Club_Title_Record\" GROUP BY clubid)) AND P.personid = O.personid AND C.ownerid = O.ownerid')
  print '2'
  player = players.fetchone() 
  print player[0]
  playerData = []
  # managerIds = g.conn.execute(text(cmd), clubId = clubid)
  # cmd = 'SELECT p1.fname AS playerfname, p1.lname AS playerlname, pc.clubId AS playerclubId, C.name, p1.personid AS personid FROM \"Player\" p, \"Person\" p1, \"Player_Of_Club\" PC, \"Club\" C WHERE p.personid = p1.personid AND p.playerid = PC.playerid AND pc.clubid = c.clubid and C.clubid = :clubId;'
  # playerIds = g.conn.execute(text(cmd), clubId = clubid)
  # temp = []
  # playerData = []
  # managerIdsCopy = []
  # playerIdsCopy = []
  # for managerId in managerIds:
  #   temp = (str(managerId[0]), str(managerId[1]),str(managerId[2]))
  #   managerIdsCopy.append(temp)
  # managerIds.close()
  # for playerId in playerIds:
  #   temp = (str(playerId[0]), str(playerId[1]),str(playerId[2]),str(playerId[3]),str(playerId[4]))
  #   playerIdsCopy.append(temp)
  # playerIds.close()
  # for managerId in managerIdsCopy:  
  #   for playerId in playerIdsCopy:
  #     if managerId[2] == playerId[4]:
  #       temp = (str(playerId[0]), str(playerId[1]))
  #       playerData.append(temp)
  #   playerIds.close()
  # managerIds.close()
  context = dict(data = playerData)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("club_player.html", **context)


@app.route('/clubs',methods=['GET'])
def clubs():
  cursor = g.conn.execute('SELECT * FROM \"Club\"')
  names = []
  temp = []
  for result in cursor:
    temp = (str(result['name']),str(result['country']),str(result['clubid']),str(result['ref_source']))
    names.append(temp)  # can also be accessed using result[0]
    print temp
  cursor.close()
  context = dict(data = names)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("clubs.html", **context)

@app.route('/managers',methods=['GET'])
def managers():
  managers = g.conn.execute('SELECT managerid, debut, personid FROM \"Manager\";')
  names = []
  temp = []
  for manager in managers:
    cmd1 = 'SELECT clubid, managerid, tenure_start, tenure_end FROM \"Club_Manager\" where managerid = :managerId;'
    clubs = g.conn.execute(text(cmd1), managerId = manager['managerid'])
    club = clubs.fetchone();
    cmd2 = 'SELECT clubid, name, country FROM \"Club\" where clubid = :clubId;'
    clubDetails = g.conn.execute(text(cmd2), clubId = club['clubid'])
    clubDetail = clubDetails.fetchone();
    clubname = str(clubDetail['name'])
    clubcountry = str(clubDetail['country'])
    cmd3 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
    persons = g.conn.execute(text(cmd3), personId = manager['personid'])
    person = persons.fetchone();
    temp = (str(person['fname']), str(person['lname']), str(person['nationality']), clubname, clubcountry, str(person['ref_source']))
    names.append(temp)  # can also be accessed using result[0]
  managers.close()
  context = dict(data = names)
  return render_template("manager.html" , **context)


@app.route('/titles',methods=['GET'])
def titles():
  cursor = g.conn.execute('SELECT titleid, inception, titlename, ref_source FROM \"Title\";')
  names = []
  temp = []
  for result in cursor:
    temp = (str(result['titlename']),str(result['inception']), str(result['ref_source']))
    names.append(temp)  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("titles.html" , **context)

@app.route('/organizations',methods=['GET'])
def organizations():
  orgs = g.conn.execute('SELECT orgid, orgname FROM \"Organization\";')
  names = []
  temp = []
  for org in orgs:
    cmd1 = 'SELECT clubid, isprimary, orgid, sponsor_start, sponsor_end FROM \"Club_Org_Sponsor_Record\" where orgid = :orgId;'
    clubs = g.conn.execute(text(cmd1), orgId = org['orgid'])
    club = clubs.fetchone();
    if club is None:
      print 'This is the shiz'
      clubname = ''
      clubcountry = ''
    else:
      print club['clubid']
      cmd2 = 'SELECT clubid, name, country FROM \"Club\" where clubid = :clubId;'
      clubDetails = g.conn.execute(text(cmd2), clubId = club['clubid'])
      clubDetail = clubDetails.fetchone();
      clubname = str(clubDetail['name'])
      clubcountry = str(clubDetail['country'])
    temp = (str(org['orgname']), clubname, clubcountry)
    names.append(temp)  # can also be accessed using result[0]
  orgs.close()
  context = dict(data = names)
  return render_template("organization.html" , **context)

@app.route('/owners',methods=['GET'])
def owners():
  owners = g.conn.execute('SELECT ownerid, personid FROM \"Owner\";')
  titleOwners = g.conn.execute('SELECT P.fname, P.lname, (SELECT count(*) AS total_titles FROM "Club_Title_Record" R WHERE C.clubid = R.clubid GROUP BY clubid), P.ref_source as ref_source FROM \"Owner\" O, \"Club_Owner\" C, \"Person\" P WHERE C.clubid = (SELECT A.clubid AS clubid FROM (SELECT clubid, count(*) AS COUNT FROM \"Club_Title_Record\" GROUP BY clubid)A WHERE A.COUNT >= ALL (SELECT COUNT(*) AS COUNT FROM \"Club_Title_Record\" GROUP BY clubid)) AND P.personid = O.personid AND C.ownerid = O.ownerid')
  titleOwnerDetails = []
  names = []
  temp = []
  for owner in owners:
    cmd2 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
    persons = g.conn.execute(text(cmd2), personId = owner['personid'])
    person = persons.fetchone();
    cmd = 'SELECT clubid FROM \"Club_Owner\" where ownerid = :ownerId;'
    clubdIds = g.conn.execute(text(cmd), ownerId = owner['ownerid'])
    clubId = clubdIds.fetchone();
    cmd3 = 'SELECT clubid, name, country FROM \"Club\" where clubid = :clubId;'
    clubs = g.conn.execute(text(cmd3), clubId = clubId['clubid'])
    club = clubs.fetchone();
    temp = (str(person['fname']), str(person['lname']), str(person['nationality']), str(club['name']), str(club['country']), str(person['ref_source']))
    names.append(temp)  # can also be accessed using result[0]
  owners.close()
  for titleOwner in titleOwners:
    temp = (str(titleOwner[0]), str(titleOwner[1]) ,str(titleOwner[2]),str(titleOwner[3]))
    titleOwnerDetails.append(temp)
  context = dict(data = names, bestOwners = titleOwnerDetails)
  return render_template("owner.html" , **context)


@app.route('/players',methods=['GET'])
def players():
  players = g.conn.execute('SELECT playerid, pos, rating, height, weight, personid FROM \"Player\";')
  bestplayers = g.conn.execute('SELECT fname AS name, lname as name1, nationality, rating, Pr.ref_source FROM \"Player\" P, \"Person\" Pr, \"Player_Of_Club\" Pc WHERE clubid IN (SELECT clubid FROM (SELECT clubid, count(*) AS COUNT FROM \"Club_Title_Record\" GROUP BY clubid) A ORDER BY A.count DESC LIMIT 5) AND P.rating > 8.2 AND P.personid = Pr.personid AND P.playerid = Pc.playerid')
  names = []
  bestPlayerData = []
  temp = []
  for player in players:
    cmd2 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
    persons = g.conn.execute(text(cmd2), personId = player['personid'])
    person = persons.fetchone();
    print player['playerid']
    cmd = 'SELECT clubid FROM \"Player_Of_Club\" where playerid = :playerId;'
    clubdIds = g.conn.execute(text(cmd), playerId = player['playerid'])
    clubId = clubdIds.fetchone();
    print clubId['clubid']
    cmd3 = 'SELECT clubid, name, country FROM \"Club\" where clubid = :clubId;'
    clubs = g.conn.execute(text(cmd3), clubId = clubId['clubid'])
    club = clubs.fetchone();
    temp = (str(person['fname']), str(person['lname']), str(person['nationality']), str(club['name']), str(player['pos']),str(player['rating']),str(player['height']),str(player['weight']),person['ref_source'])
    #print temp
    names.append(temp)  # can also be accessed using result[0]
  players.close()
  for bestplayer in bestplayers:
    temp = (str(bestplayer[0]), str(bestplayer[1]) ,str(bestplayer[2]), str(bestplayer[3]),str(bestplayer[4]))
    bestPlayerData.append(temp)
    print temp
  bestplayers.close()
  context = dict(data = names , bestPlayers = bestPlayerData)
  return render_template("player.html" , **context)

@app.route('/club',methods=['GET'])
def club():
  print request.args
  clubid = str(request.args['club_id'])
  print clubid
  temp = []
  managerData = []
  ownerData = []
  cmd = 'SELECT playerid FROM \"Player_Of_Club\" where clubid = :clubid;'
  playerIds = g.conn.execute(text(cmd), clubid = clubid)
  cmd = 'SELECT ownerid FROM \"Club_Owner\" where clubid = :clubid;'
  owners = g.conn.execute(text(cmd), clubid = clubid)
  owner = owners.fetchone();
  cmd = 'SELECT managerid FROM \"Club_Manager\" where clubid = :clubid;'
  managers = g.conn.execute(text(cmd), clubid = clubid)
  manager = managers.fetchone();
  cmd = 'SELECT personid FROM \"Owner\" where ownerid = :ownerId;'
  ownerIds = g.conn.execute(text(cmd), ownerId = owner['ownerid'])
  ownerId = ownerIds.fetchone();
  cmd = 'SELECT personid FROM \"Manager\" where managerid = :managerId;'
  managers = g.conn.execute(text(cmd), managerId = manager['managerid'])
  manager = managers.fetchone();
  cmd2 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
  owners = g.conn.execute(text(cmd2), personId = ownerId['personid'])
  owner = owners.fetchone();
  print manager['personid']
  cmd2 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
  personManagers = g.conn.execute(text(cmd2), personId = manager['personid'])
  personManager = personManagers.fetchone();


  cmd = 'SELECT C.name AS managerClubname,MC.clubid AS managerclubid,p2.personId AS personId, P2.ref_source as ref_source FROM \"Manager\" M, \"Person\" P2, \"Club_Manager\" MC, \"Club\" C WHERE M.personId = p2.personId AND MC.managerId = M.managerId AND MC.clubid = C.clubid and C.clubid = :clubId;'
  managerIds = g.conn.execute(text(cmd), clubId = clubid)
  cmd = 'SELECT p1.fname AS playerfname, p1.lname AS playerlname, pc.clubId AS playerclubId, C.name, p1.personid AS personid, p1.ref_source as ref_source FROM \"Player\" p, \"Person\" p1, \"Player_Of_Club\" PC, \"Club\" C WHERE p.personid = p1.personid AND p.playerid = PC.playerid AND pc.clubid = c.clubid and C.clubid = :clubId;'
  playerIdsJoin = g.conn.execute(text(cmd), clubId = clubid)
  temp = []
  interestingPlayerData = []
  managerIdsCopy = []
  playerIdsCopy = []
  for managerId in managerIds:
    temp = (str(managerId[0]), str(managerId[1]),str(managerId[2]), str(managerId[3]))
    managerIdsCopy.append(temp)
  managerIds.close()
  for playerId in playerIdsJoin:
    temp = (str(playerId[0]), str(playerId[1]),str(playerId[2]),str(playerId[3]),str(playerId[4]),str(playerId[5]))
    playerIdsCopy.append(temp)
  playerIdsJoin.close()
  for managerId in managerIdsCopy:  
    for playerId in playerIdsCopy:
      if managerId[2] == playerId[4]:
        temp = (str(playerId[0]), str(playerId[1]),str(playerId[5]))
        interestingPlayerData.append(temp)
        print interestingPlayerData
  temp = (str(owner['fname']), str(owner['lname']),str(owner['ref_source']));
  temp1 = (str(personManager['fname']), str(personManager['lname']),str(personManager['ref_source']));
  ownerData.append(temp1);
  ownerData.append(temp);
  
  playerData = []
  for playerId in playerIds:
    cmd1 = 'SELECT playerid, pos, rating, height, weight, personid FROM \"Player\" where playerid = :playerId;'
    players = g.conn.execute(text(cmd1), playerId = playerId['playerid'])
    player = players.fetchone();
    cmd2 = 'SELECT fname, lname, personid, dob, nationality, ref_source FROM \"Person\" where personid = :personId;'
    persons = g.conn.execute(text(cmd2), personId = player['personid'])
    person = persons.fetchone();
    temp = (str(person['fname']), str(person['lname']), str(person['nationality']), str(player['pos']),str(player['rating']),str(player['height']),str(player['weight']),str(person['ref_source']))
    playerData.append(temp)
    print playerData
  playerIds.close() 
  context = dict(data = playerData, data1 = ownerData, data2 = interestingPlayerData)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("club_player.html", **context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
