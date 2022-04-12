node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image ===============') {
    app = docker.build("chungil987/raspberry:muyaho")
  }
  
  stage('============== Push image ===============') {
    docker.withRepository('chungil987/raspberry', '	2375cfc7-0c3c-414d-99c3-e6d8f2417e34') {
      app.push()
    }
  }
}
