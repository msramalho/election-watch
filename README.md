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
docker exec some-mongo sh -c 'exec mongodump -d election --archive' > PATHTOLOCALFILE/dump.archive
```

```bash
docker exec -it election-watch_core_1 bash
```

### Pre-commit
Check [pre-commit.com](https://pre-commit.com/hooks.html) for more pre-commit functionality and then add it to the [pre-commit config file](.pre-commit-config.yaml).

To run, execute `pre-commit run --all-files`.
