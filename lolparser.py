import requests
import datetime
import re
from pymongo import Connection
from BeautifulSoup import BeautifulSoup

class Player:
  def __init__(self, name, rank, wins, losses, rating):
    self.name = name
    self.rank = rank
    self.wins = wins
    self.losses = losses
    self.rating = rating
    self.parsedDate = datetime.datetime.utcnow()

  def toJSON(self):
    return { "name" : self.name, "rank" : self.rank, "wins": self.wins, "losses": self.losses, "rating": self.rating, "parsedDate" : self.parsedDate }


class PlayerParser:
  def parse(self, row):
    name = row.find("td", { "class" : re.compile(r"views-field-summoner-name-1")}).string.strip()
    rank = int(row.find("td", { "class" : re.compile(r"views-field-rank")}).string.replace(',',''))
    wins = int(row.find("td", { "class" : re.compile(r"views-field-wins")}).string)
    losses = int(row.find("td", { "class" : re.compile(r"views-field-losses")}).string)
    rating = int(row.find("td", { "class" : re.compile("views-field-rating")}).string)
    return Player(name, rank, wins, losses, rating)

class DBSaver():
  def __init__(self, host, port, database):
    connection = Connection(host, port)
    self.db = connection[database]

  def save(self, player):
    self.db.players.insert(player.toJSON())

class LoLParser:
  def __init__(self, url, dbSaver, parseRange, playerParser):
    self.url = url
    self.dbSaver = dbSaver
    self.parseRange = parseRange
    self.playerParser = playerParser

  def run(self):
    for i in self.parseRange: 
      r = requests.get(self.url + str(i))
      soup = BeautifulSoup(r.content)
      body = soup.find("tbody")
      rows = body.findAll("tr")
      for row in rows:
        self.dbSaver.save(self.playerParser.parse(row))

def __main__():
  dbSaver = DBSaver("localhost", 27017, "lolranking")
  playerParser = PlayerParser()
  url = "http://competitive.euw.leagueoflegends.com/ladders/euw/current/rankedsolo5x5?summoner_name=&page="
  lolParser = LoLParser(url, dbSaver, range(0, 6342), playerParser)
  lolParser.run()


if __name__ == "__main__":
  __main__()
