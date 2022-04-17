node {
  stage('============== Clone repository ===============') {
    checkout scm
  }
  
  stage('============== Build image & push ===============') {
    sh 'docker login -u chungil987 -p ${PASSWORD}'
    sh 'docker build -t chungil987/muyaho:${VERSION} .'
    sh 'docker push chungil987/muyaho:${VERSION}'
  }

  stage('============== deploy image ==============') {
    try{
      sh 'sudo k3s kubectl set image deployment/muyaho-deploy muyaho=chungil987/muyaho:${VERSION}'
    } catch(Exception err) {
      def data = 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: muyaho-deploy\n  labels:\n    app: muyaho-deploy\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: muyaho-deploy\n  template:\n    metadata:\n      labels:\n        app: muyaho-deploy\n    spec:\n      containers:\n      - name: muyaho\n        image: chungil987/muyaho:' + ${VERSION} + '\n        args: ["' + ${TOKEN} + '"]'
      writeFile(file: 'muyaho.yaml', text: data)
      sh 'sudo k3s kubectl apply -f muyaho.yaml'
    }
  }
}
