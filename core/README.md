# Restore MongoDb from backup
```
docker exec -i <CONTAINER> sh -c 'mongorestore --uri="mongodb://USER:PASS@localhost:27017/" --gzip' < <DUMP_FOLDER>
mongorestore --uri="mongodb://USER:PASS@localhost:27017/" --gzip <DUMP_FOLDER>
```

windows: `mongorestore --uri="mongodb://localhost:27017/" /d electionwatch .\electionwatch\ --gzip`
windows old datasets: `mongorestore --uri="mongodb://localhost:27017/" /d electionwatch_old .\electionwatch\ --gzip`
