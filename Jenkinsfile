node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image ===============') {
    app = docker.build("chungil987/raspberry")
  }
  
  stage('============== Push image ===============') {
    docker.withRepository('https://registry.hub.docker.com', '2375cfc7-0c3c-414d-99c3-e6d8f2417e34') {
      app.push("muyaho")
    }
  }
}
