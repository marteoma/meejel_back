pipeline {
    agent { 
        dockerfile true
    }
    stages {
        stage('migrations') {
            steps {
                sh 'python manage.py migrate'
            }
        }
        stage('test') {
            steps {
                sh 'ip a'
                sh 'curl 0.0.0.0:9090'
            }
        }
    }
}