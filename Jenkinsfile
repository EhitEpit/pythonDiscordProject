node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image ===============') {
    app = docker.build("chungil987/raspberry:muyaho")
  }
  
  stage('============== Push image ===============') {
    docker.withRepository('chungil987/raspberry', '7785e67a-d7b2-4683-82bf-dc2da699140c') {
      app.push()
    }
  }
}
