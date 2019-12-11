#!/bin/bash

#pod_template_config_path='./kube/hello/HelloPod.template.yaml'
pod_template_config_path='./kube/hello_config/HelloPod.template.yaml'
service_config_path='./kube/hello/HelloService.yaml'

# 0. 定义镜像版本
image_version=`date +%Y%m%d_%H%M%S`
image_name=learnzpk/learn-k8s
image_url="${image_name}:${image_version}"

# 1. 构建镜像
docker build -t ${image_url} .
if [[ $? != 0 ]]; then
    echo "image '$image_url' build failed!"
    exit 1
fi

# 2. push镜像到远程，本地使用则不需要push
docker push ${image_url}
if [[ $? != 0 ]]; then
    echo "image '$image_url' push failed!"
    exit 1
fi

# 3. 应用pod
# 替换template中的镜像占位符
pod_config_path=`echo ${pod_template_config_path}|sed 's#\.template##'`
printf "image_url=${image_url}\ncat << EOF\n$(cat ${pod_template_config_path})\nEOF"|bash > ${pod_config_path}

# 生成pod

kubectl apply -f ${pod_config_path}
if [[ $? != 0 ]]; then
    echo "apply ${pod_config_path} failed!"
    exit 1
fi

## 4. 应用service
kubectl apply -f ${service_config_path}