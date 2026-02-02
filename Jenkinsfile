#!/usr/bin/env groovy

library identifier: 'jenkins-shared-library@main', retriever: modernSCM(
   [$class: 'GitSCMSource',
    remote: 'https://github.com/Alex1-ai/jenkins-shared-library',
    credentialsId: 'github-credentials'
   ]
)


pipeline {
    agent any

    environment {
        // Define any environment variables here
        DOCKER_IMAGE = 'chidi123/dog_prediction:1.4'
    }

    stages {
        stage('test') {
            steps {
                script {
                    echo 'This is a test stage to verify Jenkins pipeline setup.'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                script {
                    // docker.build(DOCKER_IMAGE)

                        echo "Building a docker application"
                        buildImage(env.DOCKER_IMAGE)
                        dockerLogin()
                        dockerPush(env.DOCKER_IMAGE)


                }
            }
        }
       stage('Deploy') {
            steps {
                // Deploy the application (this is a placeholder, replace with actual deployment steps)
                script {
                    def dockerCmd = "docker run -d -p 8000:8000 ${DOCKER_IMAGE}"
                    echo 'Deploying the AI Dog Prediction System...'
                    sshagent(['ec2-server-key']) {

                        // some block
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@18.205.238.229 ${dockerCmd}"

                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up resources, send notifications, etc.
            echo 'Pipeline completed.'
        }
    }
}
