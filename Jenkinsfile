pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            // Run as root inside the agent container to allow installing dependencies cleanly
            args '-u root:root'
        }
    }

    parameters {
        string(
            name: 'BRANCH_NAME',
            defaultValue: 'main',
            description: 'Git branch or tag to pull and test'
        )
        booleanParam(
            name: 'CHECK_FORMAT',
            defaultValue: true,
            description: 'Enforce strict Ruff code formatting check'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Execute unit test suite with pytest'
        )
    }

    options {
        // Discard old build history to conserve local disk space
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        // Abort build if it hangs for more than 15 minutes
        timeout(time: 15, unit: 'MINUTES')
        // Prepend timestamps to console output
        timestamps()
        // Prevent concurrent builds on the same branch
        disableConcurrentBuilds()
    }

    environment {
        // Force Python to avoid buffering stdout/stderr
        PYTHONUNBUFFERED = '1'
        // Pip cache configuration inside the workspace
        PIP_CACHE_DIR    = "${WORKSPACE}/.cache/pip"
    }

    stages {
        stage('Checkout Target Branch') {
            steps {
                echo "Fetching and checking out branch: ${params.BRANCH_NAME}..."
                sh """
                    git fetch origin ${params.BRANCH_NAME} || true
                    git checkout ${params.BRANCH_NAME} || true
                    git log -1 --oneline
                """
            }
        }

        stage('Environment Info') {
            steps {
                echo "=========================================="
                echo "Target Branch: ${params.BRANCH_NAME}"
                echo "Workspace:     ${WORKSPACE}"
                echo "Executor Node: ${NODE_NAME}"
                echo "=========================================="
                sh 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing dependencies rapidly using uv into isolated container agent..."
                sh '''
                    pip install --quiet uv
                    uv pip install --system -r requirements-dev.txt
                    ruff --version
                    pytest --version
                '''
            }
        }

        stage('Lint & Static Analysis') {
            steps {
                echo "Running Ruff code quality and linter checks..."
                sh 'ruff check .'
            }
        }

        stage('Format Verification') {
            when {
                expression { return params.CHECK_FORMAT }
            }
            steps {
                echo "Checking code format adherence with Ruff..."
                sh 'ruff format --check .'
            }
        }

        stage('Unit Tests') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                echo "Running unit test suite with pytest..."
                sh 'pytest -v tests/'
            }
        }
    }

    post {
        always {
            echo "CI pipeline completed. Cleaning temporary caches..."
            cleanWs(
                cleanWhenAborted: true,
                cleanWhenFailure: false,
                cleanWhenNotBuilt: true,
                cleanWhenSuccess: true,
                cleanWhenUnstable: false,
                deleteDirs: true,
                patterns: [[pattern: '.ruff_cache/**', type: 'INCLUDE'], [pattern: '.pytest_cache/**', type: 'INCLUDE']]
            )
        }
        success {
            echo " SUCCESS: All Ruff checks and unit tests passed cleanly!"
        }
        failure {
            echo " FAILURE: Build failed. Check the Ruff or Pytest output above."
        }
    }
}
