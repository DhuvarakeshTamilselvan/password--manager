
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
                bat 'docker build --build-arg VERSION=%VERSION% -t %IMAGE_NAME%:%VERSION% .'
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
echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin
if errorlevel 1 exit /b 1
docker push %IMAGE_NAME%:%VERSION%
if errorlevel 1 exit /b 1
docker logout
'''
                }
            }
        }
    }

    post {
        success {
            echo 'Password Manager image built and pushed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for the failing stage.'
        }
    }
}
