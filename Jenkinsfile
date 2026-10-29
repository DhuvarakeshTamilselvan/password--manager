
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
        IMAGE_NAME = 'dhuvarakesh529/password-manager'
        DOCKER_EXE = 'C:\\Users\\prana\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER_EXE%" build --build-arg VERSION=%VERSION% -t %IMAGE_NAME%:%VERSION% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat '''@echo off
"%DOCKER_EXE%" login -u %DOCKERHUB_USER% --password-stdin < nul
'''
                }
            }
        }
    }

    post {
        success {
            echo 'Password Manager image built successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
