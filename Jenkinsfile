pipeline {
    agent any

    environment {
        APP_NAME = 'it-helpdesk'
        APP_VERSION = '1.0.0'
        FRONTEND_PORT = '80'
        BACKEND_PORT = '8088'
        MYSQL_PORT = '3306'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                echo '====================================================='
                echo ' STAGE 1: Checking out IT Helpdesk Source Code'
                echo '====================================================='
                checkout scm
            }
        }

        stage('Validate Environment & Tools') {
            steps {
                echo '====================================================='
                echo ' STAGE 2: Validating Host Prerequisites and Runtimes'
                echo '====================================================='
                script {
                    if (isUnix()) {
                        sh 'java -version'
                        sh 'mvn -version'
                        sh 'node -v'
                        sh 'npm -v'
                        sh 'docker --version'
                        sh 'docker compose version'
                    } else {
                        bat 'java -version'
                        bat 'mvn -version'
                        bat 'node -v'
                        bat 'npm -v'
                        bat 'docker --version'
                        bat 'docker compose version'
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                echo '====================================================='
                echo ' STAGE 3: Compiling Spring Boot 3.2.5 Backend (Java 21)'
                echo '====================================================='
                dir('backend') {
                    script {
                        if (isUnix()) {
                            sh 'mvn clean compile'
                        } else {
                            bat 'mvn clean compile'
                        }
                    }
                }
            }
        }

        stage('Run Backend Unit & Integration Tests') {
            steps {
                echo '====================================================='
                echo ' STAGE 4: Executing Automated JUnit 5 & Mockito Tests'
                echo '====================================================='
                dir('backend') {
                    script {
                        if (isUnix()) {
                            sh 'mvn test'
                        } else {
                            bat 'mvn test'
                        }
                    }
                }
            }
        }

        stage('Build Frontend Bundle') {
            steps {
                echo '====================================================='
                echo ' STAGE 5: Installing Dependencies & Building React SPA'
                echo '====================================================='
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm ci'
                            sh 'npm run build'
                        } else {
                            bat 'npm.cmd ci'
                            bat 'npm.cmd run build'
                        }
                    }
                }
            }
        }

        stage('Validate Docker Compose') {
            steps {
                echo '====================================================='
                echo ' STAGE 6: Validating Docker Compose Orchestration Graph'
                echo '====================================================='
                script {
                    if (isUnix()) {
                        sh 'docker compose config'
                    } else {
                        bat 'docker compose config'
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '====================================================='
                echo ' STAGE 7: Building Multi-Stage Docker Images'
                echo '====================================================='
                script {
                    if (isUnix()) {
                        sh 'docker compose build'
                    } else {
                        bat 'docker compose build'
                    }
                }
            }
        }
    }

    post {
        always {
            echo '====================================================='
            echo ' POST: Publishing Automated Test Results'
            echo '====================================================='
            junit testResults: 'backend/target/surefire-reports/*.xml', allowEmptyResults: true
        }
        success {
            echo '====================================================='
            echo ' POST: Archiving Build Artifacts'
            echo '====================================================='
            archiveArtifacts artifacts: 'backend/target/*.jar,backend/target/site/jacoco/**', allowEmptyArchive: true, fingerprint: true
            echo 'BUILD SUCCESSFUL: All tests passed, bundle compiled, and Docker images built.'
        }
        failure {
            echo 'BUILD FAILED: Investigation required. Consult stage console output for diagnostic details.'
        }
    }
}
