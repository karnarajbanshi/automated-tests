pipeline {
    agent { label 'remote-node' } // Use the configured remote node

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to test') // Parameterized branch selection
    }

    environment {
        REPO_URL = 'https://github.com/karnarajbanshi/automated-tests.git' // Repository URL
        TEST_SCRIPT = 'tests/test_selenium_google.py' // Selenium test file path
        REPORT_FILE = 'report.html' // Test report file
        PATH = "/home/jenkins/.local/bin:${env.PATH}" // Include pipx in PATH
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning repository...'
                git branch: "${params.BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Verify Selenium Installation') {
            steps {
                echo 'Checking if Selenium is installed...'
                sh '''
                if ! pipx list | grep selenium; then
                    echo "Selenium not installed. Installing..."
                    pipx install selenium
                else
                    echo "Selenium is already installed."
                fi
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium tests in headless mode...'
                sh '''
                # Run the test script using pipx-managed Selenium
                pipx run --spec selenium python ${TEST_SCRIPT} --html=${REPORT_FILE} --self-contained-html
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
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } // Run only if no failures occurred
            }
            steps {
                script {
                    echo 'Automating code merge...'
                    def GITHUB_REPO = 'karnarajbanshi/automated-tests' // Replace with your repository
                    def BRANCH_TO_MERGE = "${params.BRANCH}"
                    sh '''
                    # Set Git user details
                    git config user.name "Karna Rajbanshi"
                    git config user.email "karnaraj05@gmail.com"

                    # Fetch latest changes and merge the branch
                    git fetch origin
                    git checkout main
                    git merge origin/${BRANCH_TO_MERGE}

                    # Push changes back to the repository
                    git push origin main
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs() // Clean up the workspace after every build
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Tests failed or merge conflicts detected. Notifying developer...'
            mail to: 'karna.rajbanshi@yipl.com.np',
                 subject: "Pipeline Failed: ${env.JOB_NAME}",
                 body: "Build failed at stage: ${env.STAGE_NAME}. Check Jenkins for details."
        }
    }
}

