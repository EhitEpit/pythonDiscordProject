node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image ===============') {
    def app = docker.build("chungil987/raspberry:muyaho")
  }
  
  stage('============== Push image ===============') {
    app.push()
  }
}
