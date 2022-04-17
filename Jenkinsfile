node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    sh 'docker login -u chungil987 -p ${PASSWORD}'
    sh 'docker build - chungil987/muyaho:${VERSION} TOKEN=${TOKEN} .'
    sh 'docker push chungil987/muyaho:${VERSION}'
  }

  stage('============== deploy image ==============') {
    try{
      sh 'sudo k3s kubectl set image deployment/muyaho-deploy muyaho=chungil987/muyaho:${VERSION}'
    } catch(Exception err) {
      sh 'echo """apiVersion: apps/v1
kind: Deployment
metadata:
  name: muyaho-deploy
  labels:
    app: muyaho-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: muyaho-deploy
  template:
    metadata:
      labels:
        app: muyaho-deploy
    spec:
      containers:
      - name: muyaho
        image: chungil987/muyaho:${VERSION}
        args: ["${TOKEN}"]""" > muyaho.yaml'
        sh 'sudo k3s kubectl apply -f muyaho.yaml'
    }
  }
}
