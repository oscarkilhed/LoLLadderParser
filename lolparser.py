import requests
from pymongo import Connection
from pyquery import PyQuery as pq

class Player:
  def __init__(self, name, rank, wins, losses, rating):
    self.name = name
    self.rank = rank
    self.wins = wins
    self.losses = losses
    self.rating = rating
  
  def toJSON(self):
    return { "name" : self.name, "rank" : self.rank, "wins": self.wins, "losses": self.losses, "rating": self.rating }


class RowParser:
  def parse(self, row):
    prow = pq(row)
    name = prow(".views-field-summoner-name-1").text() 
    rank = int(prow(".views-field-rank").text().replace(',',''))
    wins = int(prow(".views-field-wins").text())
    losses = int(prow(".views-field-losses").text())
    rating = int(prow(".views-field-rating").text())
    return Player(name, rank, wins, losses, rating)

class DBSaver():
  def __init__(self, host, port, database):
    connection = Connection('localhost', 27017)
    self.db = connection['lolranking']

  def save(self, player):
    self.db.players.insert(player.toJSON())

class LoLParser:
  def __init__(self, url, dbSaver, parseRange, rowParser):
    self.url = url
    self.dbSaver = dbSaver
    self.parseRange = parseRange
    self.rowParser = rowParser

  def run(self):
    for i in self.parseRange: 
      r = requests.get(self.url + str(i))
      html = pq(r.content)
      rows = html("tbody tr")
      for row in rows:
        self.dbSaver.save(self.rowParser.parse(row))

def __main__():
  dbSaver = DBSaver("localhost", 27017, "lolranking")
  rowParser = RowParser()
  url = "http://competitive.euw.leagueoflegends.com/ladders/euw/current/rankedsolo5x5?summoner_name=&page="
  lolParser = LoLParser(url, dbsaver, range(0, 6342), rowParser)
  lolParser.run()


if __name__ == "__main__":
  __main__()
