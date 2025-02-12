# Initialization
```shell
curl -X POST http://localhost:5000/powerplant/initialize -H "Content-Type: application/json" -d '{
    "location": "cal",
    "time_zone": "pacific-time"
}'

```

# Get data
```shell
curl -X GET "http://localhost:5000/powerplant/generate_power?time_step=5"


```
