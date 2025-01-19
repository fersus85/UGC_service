#!/bin/bash

# настроим серверы конфигурации
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
# docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
sleep 1
# соберём набор реплик первого шарда
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
# docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'
sleep 5
# познакомим шард с маршрутизаторами
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
sleep 1
# Второй шард добавим по аналогии. Сначала инициализируем реплики.
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
# добавим их в кластер
sleep 5
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
# docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'
sleep 5
# Создадим БД
docker exec -it mongors1n1 bash -c 'echo "use ugc2_movies" | mongosh'
sleep 1
# Включим шардирование
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugc2_movies\")" | mongosh'
sleep 1

# Создадим коллекцию
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc2_movies.film_bookmarks\")" | mongosh'
sleep 1
# Настроим шардирование по полю someField
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc2_movies.film_bookmarks\", {\"film_id\": \"hashed\"})" | mongosh'

# Создадим коллекцию
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc2_movies.film_reviews\")" | mongosh'
sleep 1
# Настроим шардирование по полю someField
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc2_movies.film_reviews\", {\"film_id\": \"hashed\"})" | mongosh'

# Создадим коллекцию
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugc2_movies.film_score\")" | mongosh'
sleep 1
# Настроим шардирование по полю someField
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugc2_movies.film_score\", {\"film_id\": \"hashed\"})" | mongosh'
