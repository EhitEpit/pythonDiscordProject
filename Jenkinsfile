node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    sh 'docker build --tag chungil987/muyaho:1.0.1 --build-arg TOKEN=${TOKEN} .'
    sh 'docker push chungil987/muyaho:1.0.1'
  }

  stage('============== deploy image ==============') {
    try{
      sh 'sudo k3s kubectl delete pod muyaho'
    } catch(Exception err) {
    }
    sh 'sudo k3s kubectl run muyaho --image chungil987/muyaho:1.0.1 --overrides="${OVERRIDE}"'
  }
}
