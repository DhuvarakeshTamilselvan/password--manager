
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select Password Manager version'
        )
    }

    environment {
        IMAGE_NAME = 'password-manager'
        DOCKER_EXE = 'C:\\Users\\prana\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
            steps {
                bat 'python --version'
                bat 'git --version'
                bat '"%DOCKER_EXE%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Check Docker Engine') {
            steps {
                bat '"%DOCKER_EXE%" info'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER_EXE%" build --build-arg VERSION=%VERSION% -t %IMAGE_NAME%:%VERSION% .'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Password Manager Docker image built.'
        }
        failure {
            echo 'FAILED: Check Console Output for the failing stage.'
        }
    }
}
