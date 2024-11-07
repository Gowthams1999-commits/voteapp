pipeline {
  agent any
  environment {
    docker_image = "thrisha24/voteapp"
    docker_version = "${BUILD_NUMBER}"
    deployment_file = "${WORKSPACE}/flask-deployment.yaml"
  }
 
  stages {
    stage('Git Checkout') {
      steps {
        git 'https://github.com/Gowthams1999-commits/voteapp.git'
      }
    }
    stage('Docker Image Build') {
      steps {
        sh 'docker build --network host -t ${docker_image}:${docker_version} .'
      }
    }
    stage('DockerHub Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'gitCred', passwordVariable: 'docker_pass', usernameVariable: 'docker_user')]) {
    sh 'echo ${docker_pass} | docker login -u ${docker_user} --password-stdin'
}
      }
    }
    stage('Docker Image Push') {
      steps {
        sh 'docker push ${docker_image}:${docker_version}'
      }
    }
    stage('Update Image in Deployment File on Server') {
      steps {
        sh 'sed -i "s|image: .*|image: ${docker_image}:${docker_version}|g" ${deployment_file}'
      }
    }
    stage('Update Docker Image to GitHub') {
      steps {
        withCredentials([string(credentialsId: 'git_token_test', variable: 'git_token_test')]) {
          sh '''
            git config --global user.name "Gowthams1999-commits"
            git config --global user.email "githubgowtham1999@gmail.com"
            git add ${deployment_file}
            git commit -m "Updated image in deployment file"
            git push https://$git_token_test@github.com/Gowthams1999-commits/voteapp.git HEAD:master
          '''
        }
      }
    }
  }
}
