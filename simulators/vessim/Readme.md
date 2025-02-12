# initialize
```shell
curl -X POST http://localhost:5000/battery/initialize -H "Content-Type: application/json" -d '{
    "capacity": 1000,
    "initial_soc": 1,
    "min_soc": 0.2,
    "c_rate": 1.0
}'


```
# update 
```shell
curl -X POST http://localhost:5000/battery/update -H "Content-Type: application/json" -d '{
    "power": -1000,
    "duration": 3600
}'

```

# get soc
```shell
curl -X GET http://localhost:5000/battery/soc

```
