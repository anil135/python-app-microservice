pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'anil135/python-app-microservice'
        DOCKER_CREDENTIALS_ID = 'docker-repo-credentials' // Docker credentials stored in Jenkins
        VENV_DIR = './venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/anil135/python-app-microservice.git'
            }
        }


        stage('Install Dependencies') {
            steps {
                //sh 'python3 -m venv ${VENV_DIR}'
                //sh 'chmod +x ${VENV_DIR}/bin/activate'
                //sh '${VENV_DIR}/bin/activate'
                //sh 'python3 -m pip install -r requirements.txt'
                sh 'pip install -r requirements.txt'
            }
        }

        
        stage('Build Docker Image') {
            steps {
                // Build the Docker image for the microservice
                sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ."
            }
        }

        
        stage('Push Docker Image') {
            steps {
                // Push the Docker image to the repository
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    '''
                }
            }
        }

    post {
        
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed. Check the logs for errors'
        }
    }
        
    }
}
