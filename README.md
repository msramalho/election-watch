<h1 align="center">Election Watch</h1>
<p align="center">A platform for monitoring democratic elections and fighting online disinformation.</p>

* [core](core/) contains the code for data collection
* [ui](ui/) contains the code for the UI, it can be automatically deployed to gh-pages. you can also use [the original UI client](https://msramalho.github.io/election-watch) if you deployed your own core collection by changing the access URL to your own.

For a full description, please check the work on which Election Watch is based: [Twitter Watch's paper](https://github.com/msramalho/twitter-watch/preliminary-paper.pdf).

## Tips and Tricks
### docker compose deploy
* `cp example.env .env` and edit
* `docker-compose up` (pass `-d` for detached mode)

### mongo dumps
```bash
docker exec some-mongo sh -c 'exec mongodump -d electionwatch --archive' > PATHTOLOCALFILE/dump.archive
```

```bash
docker exec -it election-watch_core_1 bash
```

### Pre-commit
Check [pre-commit.com](https://pre-commit.com/hooks.html) for more pre-commit functionality and then add it to the [pre-commit config file](.pre-commit-config.yaml).

To run, execute `pre-commit run --all-files`.

### Useful MongoDb queries
* database current size in GB `db.stats(1024*1024*1024).dataSize + " GB";`
* get the top 50 mentions after a given date:
```sql
db.getCollection('tweets').aggregate([
  {$match: {"original": true}},

  {$unwind: '$user_mentions'}, 

  { $group: { 
      _id: '$user_mentions',
      count: {$sum: 1}
      -- count: {$sum: { $add : ['$favorite_count', '$retweet_count']}}
  }},

  {$sort: {count: -1}},

  {$limit: 50},

  { $project: { count: 1, _id: '$_id' }}
]).map(x=>x._id + " - " + db.getCollection('users').find({_id: x._id}).map(y=>y.screen_name) +  " - " + x.count).reduce((acc, prev) => acc + "\n" + prev)
```
* get the top 50 hashtags by either impact (retweets + favorites) or just appearance count
```javascript
db.getCollection('tweets').aggregate([
  {$match: {"original": true}},
  {$unwind: '$hashtags'}, 
  { $group: { 
      _id: '$hashtags',
      count: {$sum: 1}, // em quantos originais aparecem
      countWeight: {$sum: { $add : ['$favorite_count', '$retweet_count']}} // retweets+favorite
  }},
  {$project: {
      impact: { $divide: [ "$countWeight", "$count" ] },
      count: 1, countWeight: 1, _id: '$_id'
   }},
   {$match: {count : {$gte: 100}}},
  {$sort: {impact: -1}}, {$limit: 50},

  { $project: { count: 1, countWeight: 1, impact: 1, _id: '$_id'}}
]).map(x=>"#" + x._id + "(" + x.impact + ") - " + x.count + " - " + x.countWeight).reduce((acc, prev) => acc + "\n" + prev)
```
* unset a given property(ies): `db.getCollection('users').update({}, {$unset: {private: 1, time_private: 1}}, {multi: true})`
* get large contributors not in seed: `db.getCollection('users').count({followers_count: {$gt: 500000}, depth: {$gt: 0}})`
* find tweets with a given hashtag(s) on a given date range `db.getCollection('tweets').find({"created_at": {$gte: new Date("2020-09-18"), $lt: new Date("2020-09-19")}, hashtags: {$in: ["HASHTAG"]}})`
* get list of ids from a query `db.getCollection('users').find({followers_count: {$gte: 100000}}, {_id: 1}).map(function(item){ return item._id; }).reduce(function(acc, prev){return acc + "," + prev})`
* get users with >= 100k followers and their follows_political, follows_news count `db.getCollection('users').find({followers_count: {$gte: 100000}, depth: {$gt: 0}}).map(x=>x.screen_name + " - " + x.follows_political + " - " + x.follows_news);`

```javascript

db.getCollection('tweets').find({hashtags: {$exists: true}})
.forEach(function(tweet) {
    tweet.hashtags = tweet.hashtags.map(function(h) {
        return h.toLowerCase();         
    }); 
    db.getCollection('tweets').save(tweet); 
})
```
````javascript
db.getCollection('users').count({
    "count_parsed_tweets": {"$gte": 25},
    "most_common_language": {"$not": {"$in": ["pt", "und"]}},
    $and: [
    {$or: [
        {follows_political: {$lte: 2}},
        {follows_political: {$exists: false}}
    ]},
    {"$or": [
        {"tweeted_languages.pt": {"$exists": false}},
        {"tweeted_languages.pt": {"$lte": 5}}
    ]}
    ]
})//.limit(200).map(x=>x.screen_name + ":" + x.follows_political + "," + x.follows_news + " - " + x.description).reduce((acc, prev) => acc + "\n" + prev)
```