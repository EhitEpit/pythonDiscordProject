node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    def app = docker.build("chungil987/raspberry:muyaho", "--build-arg TOKEN=${TOKEN}")
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
        app.push("muyaho")
    }
  }

  stage('============== deploy image ==============') {
    sh 'sudo cd /home/pi'
    sh 'sudo k3s kubectl delete pod muyaho-pod'
    sh 'sudo k3s kubectl apply -f rasp.yaml'
  }
}
