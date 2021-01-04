# elastic_mysql_flask

### Running

1. Setup the configurations for elasticsearch on: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144

Look at your system to properly setup vm.max_map_count

2. run `docker-compose up -d` in the project root

3. Load the mysql dump by running inside the test_db folder: 

* `docker exec -i containerId mysql -uroot -pchangeme employees < load_departments.dump`