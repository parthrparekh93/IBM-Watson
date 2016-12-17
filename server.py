#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

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

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
