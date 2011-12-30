//This mongo shell script performes a map reduce to enable some graphing of the rating distribution

map = function(){
  emit({}, {list : [{ rating: this.rating - this.rating % 10, count: 1 }]})
};

reduce = function(keys, vals){
  ratings = {}
  for(var i = 0; i< vals.length; i++){
    var currentlist = vals[i].list;
    for(var x = 0; x < currentlist.length; x++){
      ratings[currentlist[x].rating] = (ratings[currentlist[x].rating] || 0) + currentlist[x].count;
    }
  } 
  list = []
  for(kvp in ratings){
    list.push({ rating: kvp, count: ratings[kvp] });
  }
  box = {list : list};
  return box;
};

var res = db.runCommand({
  mapreduce: "players",
  map: map,
  reduce: reduce,
  out: "playersPerRating",
  verbose: true
  });

