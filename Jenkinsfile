node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    def app = docker.build("chungil987/raspberry:muyaho")
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
        app.push("muyaho")
    }
  }

  stage('============== deploy image ==============') {
    sh 'sudo k3s kubectl delete pod muyaho-pod'
    sh 'pwd'
    sh 'sudo k3s kubectl apply -f rasp.yaml'
  }
}
