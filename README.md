# Demo Nifi, Kafka, Confluent

This repo contains a demo setup with Nifi, Kafka and the [Confluent platform](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html). These services can be run directly with [Docker compose](https://www.docker.com/get-started/). Overview:

![Overview](images/overview.png)

## Run

Run all the applications with (-d means `detached` and is used to not display the stdout, see [reference](https://docs.docker.com/compose/reference/)):

```
docker-compose up -d
```

In case of conflicts or problems run `docker system prune`

Check if everything is working:

```
docker-compose ps
```

Show logs:

```
docker-compose logs -f <app>
```

### Dashboards

- [Nifi](https://localhost:8443/nifi) (login with admin/S3curePa55word)
- [Confluent Control Center](http://localhost:9021/)

## Stop

Stop with:

```
docker-compose down
```
