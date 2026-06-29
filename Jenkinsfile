pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build and Deploy') {
            steps {
                echo 'Building and deploying with Docker Compose...'
                sh '''
                    docker compose down
                    docker compose up --build -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Checking application health...'
                sh '''
                    sleep 10
                    curl -f http://localhost/health
                '''
            }
        }
    }
}
