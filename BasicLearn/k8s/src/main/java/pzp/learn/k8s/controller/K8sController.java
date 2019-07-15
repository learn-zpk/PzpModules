package pzp.learn.k8s.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pzp.learn.k8s.service.K8sService;

/**
 * @author learnzpk
 * @date 2019/03/24
 * @description
 */
@RestController
@RequestMapping("/k8s")
public class K8sController {
    @Autowired
    private K8sService service;

    @RequestMapping(value = "/hello")
    public Object sayHello() {
        return service.sayHello();
    }

    @RequestMapping(value = "/helloMongo")
    public Object sayHelloMongo() {
        return service.sayHelloMongo();
    }
}
