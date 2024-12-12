pipeline {
    agent any
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to test')
    }
    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        REPORT_FILE = "report.html"
    }
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning repository...'
                git branch: "${params.BRANCH}", url: 'https://github.com/karnarajbanshi/automated-tests.git'
            }
        }
        stage('Run Selenium Tests') {
            steps {
                echo 'Setting up virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
                echo 'Running Selenium tests...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest --html=${REPORT_FILE} --self-contained-html
                '''
            }
            post {
                always {
                    echo 'Archiving test results...'
                    archiveArtifacts artifacts: "${REPORT_FILE}", fingerprint: true
                }
                success {
                    echo 'Tests passed successfully!'
                }
                failure {
                    echo 'Tests failed! Check the test report for details.'
                    error 'Stopping pipeline due to test failure.'
                }
            }
        }
        stage('Automate Merge') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    def GITHUB_REPO = 'karnarajbanshi/automated-tests' // Replace with your repo
                    def PR_NUMBER = 'replace-with-pr-number' // Replace with the PR number or use Git logic
                    sh """
                        curl -X PUT -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{"merge_method": "squash"}' \
                            https://api.github.com/repos/${GITHUB_REPO}/pulls/${PR_NUMBER}/merge
                    """
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Investigate the logs for details.'
        }
    }
}

