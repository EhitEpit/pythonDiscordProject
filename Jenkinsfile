node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    def app = docker.build("chungil987/raspberry:muyaho", "--build-arg TOKEN=${TOKEN} .")
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
        app.push("muyaho")
    }
  }

  dir('/home/pi'){
      stage('============== deploy image ==============') {
        try{
          sh 'sudo k3s kubectl delete pod muyaho-pod'
        } catch(Exception err) {

        }
        sh 'sudo k3s kubectl apply -f rasp.yaml'
      }
  }

}
