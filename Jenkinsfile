def notifyBuild(String buildStatus = 'STARTED') {
  // build status of null means successful
  buildStatus = buildStatus ?: 'SUCCESS'

  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

  // Override default values based on build status
  if (buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'SUCCESS') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }

  emailext (
      subject: subject,
      body: details,
      to: 'chungil987@naver.com'
    )
}

node {
  try{
    stage('============== Clone repository ===============') {
      notifyBuild('STARTED')
      checkout scm
    }

    stage('============== Build image & push ===============') {
        sh 'docker login -u chungil987 -p ${PASSWORD}'
        sh 'docker build -t chungil987/muyaho:${VERSION} .'
        sh 'docker push chungil987/muyaho:${VERSION}'
        sh 'docker rmi chungil987/muyaho:${VERSION}'
    }

    stage('============== deploy image ==============') {
      try{
        sh 'sudo k3s kubectl set image deployment/muyaho-deploy muyaho=chungil987/muyaho:${VERSION}'
      } catch(Exception err) {
        def data = 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: muyaho-deploy\n  labels:\n    app: muyaho-deploy\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: muyaho-deploy\n  template:\n    metadata:\n      labels:\n        app: muyaho-deploy\n    spec:\n      containers:\n      - name: muyaho\n        image: chungil987/muyaho:1.0.' + "${BUILD_NUMBER}" + '\n        args: ["' + "${params.TOKEN}" + '"]'
        writeFile file: 'muyaho.yaml', text: data
        sh 'sudo k3s kubectl apply -f muyaho.yaml'
      }
    }
    stage('============== ===') {
      notifyBuild('SUCCESS')
    }
  } catch(Exception err) {
    currentBuild.result = "FAILED"
    throw err
  } finally {
    notifyBuild(currentBuild.result)
  }
}
