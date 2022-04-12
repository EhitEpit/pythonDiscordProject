node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image ===============') {
    def app = docker.build("chungil987/raspberry:muyaho")
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
        app.push("muyaho")
    }
  }
}
