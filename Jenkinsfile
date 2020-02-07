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
    }
}