pipeline {
    agent any
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to test')
    }
    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        REPORT_FILE = "report.html"
        GITHUB_TOKEN = credentials('github_token')  // Store your GitHub token in Jenkins credentials
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
                    // Authenticate with GitHub
                    sh """
                        gh auth login --with-token <<< "${GITHUB_TOKEN}"
                    """
                    
                    // Get the PR number dynamically using the branch name
                    def PR_NUMBER = sh(script: """
                        gh pr list --state open --head ${params.BRANCH} --json number -q '.[0].number'
                    """, returnStdout: true).trim()
                    
                    if (PR_NUMBER) {
                        echo "Found PR number: ${PR_NUMBER}"
                        // Merge the PR using the GitHub CLI (squash and delete the branch after merge)
                        sh """
                            gh pr merge ${PR_NUMBER} --squash --delete-branch
                        """
                    } else {
                        echo "No open PR found for branch: ${params.BRANCH}"
                    }
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

