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


        stage('Setup Virtual Environment') {
            steps {
                // Create the virtual environment
                sh 'sudo apt update'
                sh 'sudo apt install python3-venv -y'
                sh 'python3 -m venv ${VENV_DIR}'
                
                // Install pip if it's missing
                sh '''
                    if [ ! -f "${VENV_DIR}/bin/pip" ]; then
                        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                        ${VENV_DIR}/bin/python get-pip.py
                    fi
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                // Activate virtual environment and install dependencies
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        
        stage('Build Docker Image') {
            steps {
                // Build the Docker image for the  python microservice
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

    }

    post {
        
        success {
            echo 'Pipeline completed successfully, Docker image pushed to anil135 repository.'
        }

        failure {
            echo 'Pipeline failed. Check logs for errors'
        }
    }
        
}
