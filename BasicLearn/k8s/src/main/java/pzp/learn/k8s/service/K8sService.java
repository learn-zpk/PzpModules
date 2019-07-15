package pzp.learn.k8s.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import java.util.Set;

/**
 * @author learnzpk
 * @date 2019/03/24
 * @description
 */
@Service
public class K8sService {
    @Autowired
    private MongoTemplate mongoTemplate;

    public Object sayHello() {
        return "Hello World!";
    }

    public String sayHelloMongo() {
        Set<String> collNames = mongoTemplate.getCollectionNames();

        // return "Hello ".concat(String.join(";", collNames));
        return "Hello,Mongo have ".concat(String.valueOf(collNames.size())).concat(" collection!");
    }
}
