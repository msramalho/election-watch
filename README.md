<h1 align="center"><img align="" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg"> Twitter Watch</h1>
<p align="center">A framework for Twitter data collection.</p>

* [core](core/) contains the code for data collection
* [ui](ui/) contains the code for the UI, it can be automatically deployed to gh-pages. you can also use [the original UI client](https://msramalho.github.io/twitter-watch) if you deployed your own core collection by changing the access URL to your own.

For a full description, please check the preliminary version of Twitter Watch's [paper](preliminary-paper.pdf).

<!-- If you use this tool academically, you can cite it through:
```bibtex
{

}
``` -->

## Architecture
The current version merges the core and api containers but you can use the version in the original architecture by using the docker-compose-2.yml file and commenting the second line in the [launcher.sh](core/launcher.sh) file (`nohup python api/main.py > logs_flask.txt &`).

<p align="center"><img src="https://i.imgur.com/7Fj4L0J.png"/></p>


## UI
<p align="center"><img src="https://i.imgur.com/yVo1Mr1.png"/></p>

## Implementation
The overall implementation is a sequential execution of groups of tasks until the scheduled (and parallel) tasks are reached.
<p align="center"><img src="https://i.imgur.com/yeF2A82.png"/></p>

## Practical results
This tool was used to collect data on the Portuguese Twittersphere, the following figure summarizes the amount of accounts and tweets it collected.
<p align="center"><img src="https://i.imgur.com/BaBEJGZ.png"/></p>

## Tips and Tricks
### docker compose deploy
* `cp example.env .env` and edit
* `docker-compose up` (pass `-d` for detached mode)

### mongo dumps
```bash
docker exec some-mongo sh -c 'exec mongodump -d twitter --archive' > PATHTOLOCALFILE/dump.archive
```

```bash
docker exec -it twitter-watch_core_1 bash
```

### Pre-commit
Check [pre-commit.com](https://pre-commit.com/hooks.html) for more pre-commit functionality and then add it to the [pre-commit config file](.pre-commit-config.yaml).

To run, execute `pre-commit run --all-files`.
