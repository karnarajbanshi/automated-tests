pipeline {
    agent { label 'remote-node' } // Set to your configured remote node
    environment {
        REPO_URL = 'https://github.com/karnarajbanshi/automated-tests.git' // Replace with your repository
        BRANCH = 'main' // Specify your branch
        TEST_SCRIPT = 'tests/test_selenium_google.py' // Path to your Selenium test file
    }
    triggers {
        cron('H 13 * * *') // Schedule: Daily at 1:00 PM
    }
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning repository...'
                git branch: "${BRANCH}", url: "${REPO_URL}"
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
                pipx run --spec selenium python ${TEST_SCRIPT}
                '''
            }
        }
        stage('Simulate Merge (Success)') {
            when {
                expression { currentBuild.result == null } // Run only if no failures occurred
            }
            steps {
                echo 'Tests successful. Code can be merged!'
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

