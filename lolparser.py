import requests
from pymongo import Connection
from pyquery import PyQuery as pq

url = "http://competitive.euw.leagueoflegends.com/ladders/euw/current/rankedsolo5x5?summoner_name=&page="

class Player:
  def __init__(self, name, rank, wins, losses, rating):
    self.name = name
    self.rank = rank
    self.wins = wins
    self.losses = losses
    self.rating = rating
  
  def toDbObject(self):
    return { "name" : self.name, "rank" : self.rank, "wins": self.wins, "losses": self.losses, "rating": self.rating }


def parse():
  connection = Connection('localhost', 27017)
  db = connection['lolranking']
  players = db.players
  for i in range(0, 6342): 
    r = requests.get(url + str(i))
    html = pq(r.content)
    rows = html("tbody tr")
    for row in rows:
      prow = pq(row)
      name = prow(".views-field-summoner-name-1").text() 
      rank = int(prow(".views-field-rank").text().replace(',',''))
      wins = int(prow(".views-field-wins").text())
      losses = int(prow(".views-field-losses").text())
      rating = int(prow(".views-field-rating").text())
      players.insert(Player(name, rank, wins, losses, rating).toDbObject())
    if i != 0 and i % 10 == 0:
      print str(i / float(6342) * 100) + "%"

def __main__():
  parse()

if __name__ == "__main__":
  __main__()
