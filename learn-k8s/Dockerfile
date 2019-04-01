FROM learnzpk/maven

MAINTAINER learnzpk

RUN echo "Asia/Shanghai" > /etc/timezone

# VOLUME ["/infer_result"]

# 不建议拷贝项目下的所有文件
COPY ./src /origin/src
COPY ./pom.xml /origin/pom.xml
# COPY ./kubernetes入门: 部署Hello World程序.md /origin/kubernetes入门: 部署Hello World程序.md

RUN cd /origin && mvn clean install && mkdir /opt && cp /origin/target/*.jar /opt/ && rm -rf /origin

WORKDIR /opt

# ENTRYPOINT无法被覆盖
# ENTRYPOINT java -jar -Xmx700m /opt/*.jar
CMD java -jar -Xmx700m /opt/*.jar