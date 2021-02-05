# Dataset 01 - Portuguese Presidential Elections, Jan 24th 2021

<h2 align="center"><a href="https://drive.google.com/u/4/uc?id=1mpm6zXLxavF88DPpp6Xn5Q4zgl8Vobr3&export=download">Download 9.5GB 📂</a></h2>


This dataset contains tweets and users mostly from the Portuguese Twittersphere. The watched users stem from a seed of political accounts (`usernames`) and news sources(`usernames_news`) (see list in the [config below](#config))


| Property               | Description                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| event                  | [Portuguese Presidential Elections, Jan 24th 2021 on Wikipedia](https://en.wikipedia.org/wiki/2021_Portuguese_presidential_election) |
| collection start       | Sep 2nd 2020                                                                                                                         |
| collection end         | Jan 30th 2021                                                                                                                        |
| code release           | [v1.0](https://github.com/msramalho/election-watch/releases/tag/v1.0)                                                                |
| code branch archive    | [branch](https://github.com/msramalho/election-watch/tree/archive-2021-presidentials)                                                |
| tweets                 | `57 155 221` (57 million)                                                                                                            |
| users                  | `1 115 491` (1 million)                                                                                                              |
| size                   | `1 115 491` (1 million)                                                                                                              |
| labels                 | `1857` `suspended` users (along with `time_suspended` date, and `time_unsuspended` in of un-suspensions)                             |
| archived API for EW UI | [election-watch-portugal-presidentials-2021](https://msramalho.github.io/election-watch-portugal-presidentials-2021)                 |
| download link          | [download 9.5GB zip](https://drive.google.com/u/4/uc?id=1mpm6zXLxavF88DPpp6Xn5Q4zgl8Vobr3&export=download)                           |
| restore command        | `mongorestore --uri="mongodb://localhost:27017/" -d ew_db ./election-watch-folder --gzip`                                            |


## Enrichments
The dataset contains labels on suspended users, and also contains a property `tweeted_languages` that contains aggregated values of tweets per language (as detected by Twitter).

# Overview
This dataset contains a period of 5 days `19/10/2020` - `24/10/2020` where the collection process was hindered, as you can see in the picture below.

![daily_tweets](https://user-images.githubusercontent.com/19508417/106947613-82722600-6722-11eb-80d3-51715b4e9be5.png)


### Config

```json
{
    "seed": {
        "usernames": ["CeuAlbuquerque", "HelgaCorreia2", "cli_as", "ainterna_pt", "_jalmeida_", "jmpureza", "Jesario1", "_tinoderans_", "ascenso_simoes", "moisesscf", "PSantanaLopes", "francisco__rs", "Partido_PAN", "proque_twit", "JoanaMortagua", "anamiguel1981", "coelho_lima1", "Telmo_Correia", "EBrilhanteDias", "KatarMoreira2", "_ERGUE_TE", "AnaPassosFaro", "FirminoMarquesB", "economia_pt", "cristovaonorte", "1956purp", "MinistroCabrita", "OsVerdes", "pdr_coimbra", "LiberalPT", "limacosta", "jprebelo_sejd", "MRMortagua", "RuiRioPSD", "cultura_pt", "partido_alianca", "JooPaul57839990", "EsquerdaNet", "carlitosbras", "pcp_pt", "ebarrocomelo", "PedroFgSoares", "AlexandraNViei1", "anabela_pedroso", "Diogo_Leao", "zmaglh", "partidochega", "ruitavares", "catarinarf", "filipenb", "AndreCVentura", "MigCMatos", "RBaptistaLeite", "paulorios65", "andrecventura", "govpt", "aapbatista", "JoaoAtaide", "DuarteMarques", "gracafonseca", "alberto_machado", "ambiente_pt", "JorgePauloOliv2", "AntonioFilipe", "FernandoRuasPE", "_CDSPP", "antoniocostapm", "DuarteCordeiro", "tbribeiro", "heloisapolonia", "PartidoTerraMPT", "pedrosizavieira", "jvstorres", "lnes_Sousa_Real", "catarina_mart", "mariofcenteno", "LaraFMartinho", "Alexandre_Poco", "jlcarneiro2009", "coelhopresident", "ppdpsd", "MariaManuelRola", "LuisVPMonteiro", "LIVREpt", "cdupcppev", "Educacao_PT", "justica_pt", "editeestrela", "monicaquintela3", "movimentojpp", "noscidadaos", "HortenseMartins", "defesa_pt", "Ana_M_MG", "PNSpedronuno", "CristasAssuncao", "jpintocoelho60", "HugCarvalho", "luismtesta", "psocialista", "AnaMartinsGomes", "BrunoARFialho", "joao_ferreira33", "mmatias_", "_tinoderans_", "LiberalMayan"],
        "usernames_news": ["lusa_noticias", "cmjornal", "dntwit", "JornalNoticias", "dnoticiaspt", "AO_Online", "Publico", "SICNoticias", "observadorpt", "tvi24pt", "RTPNoticias", "expresso", "Renascenca", "Radio_Comercial", "ojeconomico", "ECO_PT", "dinheiro_vivo", "SolOnline", "Visao_pt", "itwitting"],
    },
    "collection": {
        "seed": {
            "friends": false,
            "followers": true
        },
        "limits": {
            "max_watched_users": 1000000,
            "max_daily_increase": 5000,
            "max_daily_increase_ratio": 0.1,
            "min_appearances_before_watched": 100
        },
        "ignore_tweet_media": true,
        "oldest_tweet": "Tue Sep 1 00:00:00 +0000 2020",
        "search_languages": ["pt", "und"],
        "max_threads": 16,
        "min_tweets_before_restricting_by_language": 10
    },
    "mongodb": {
        "database": "electionswatch",
    },
}
```
