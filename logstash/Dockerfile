
FROM docker.elastic.co/logstash/logstash:7.10.1
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
ADD /mysql-lib/mysql-connector-java-5.1.36.jar /usr/share/logstash/
