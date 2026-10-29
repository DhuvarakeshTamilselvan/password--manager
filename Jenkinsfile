
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

        stage('Check Environment') {
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

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''@echo off
echo %DOCKERHUB_TOKEN%| "%DOCKER_EXE%" login -u "%DOCKERHUB_USER%" --password-stdin
if errorlevel 1 exit /b 1

"%DOCKER_EXE%" push %IMAGE_NAME%:%VERSION%
if errorlevel 1 exit /b 1

"%DOCKER_EXE%" logout
'''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Password Manager image built and pushed to Docker Hub.'
        }

        failure {
            echo 'FAILED: Check the Console Output for the failed stage.'
        }

        always {
            echo 'Password Manager Jenkins pipeline execution completed.'
        }
    }
}
