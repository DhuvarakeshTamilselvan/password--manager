pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Choose the Password Manager version to build'
        )
    }

    environment {
        // Replace with your Docker Hub username/repository.
        IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/password-manager'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --build-arg VERSION=${VERSION} -t ${IMAGE_NAME}:${VERSION} .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push "${IMAGE_NAME}:${VERSION}"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/${VERSION}.yaml'
            }
        }
    }

    post {
        always {
            echo 'Password Manager pipeline finished.'
        }
    }
}
