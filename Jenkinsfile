#!groovy

node('linux-docker') {

    def REGISTRY_IMAGE_URL="registry.gitlab.com/cds.py/icargo/icargo-v1/icargo-backend";

    def MAIN_WEBHOOKS_URL="http://51.159.176.45:19988";
    def TESTING_WEBHOOKS_URL="http://163.172.182.37:19987";
    def DESARROLLO_WEBHOOKS_URL="http://163.172.182.37:19988";

    stage('Preparation') {
        checkout scm;
    }

    stage('Pre-Build') {
        withCredentials([string(credentialsId: 'telegramToken' , variable: 'TOKEN')]) {
            withCredentials([string(credentialsId: 'telegramChatid' , variable: 'CHAT_ID')]) {
                sh "curl --location --request POST 'https://api.telegram.org/bot$TOKEN/sendMessage' --form text='Building $JOB_NAME' --form chat_id='$CHAT_ID'"
            }       
        }    
    }

    try {
        stage('Docker build') {
            if (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'testing' || env.BRANCH_NAME == 'develop') {
                def imageName = "${REGISTRY_IMAGE_URL}:${env.BRANCH_NAME}";

                docker.withRegistry('https://registry.gitlab.com', 'dante_jenkins') {
                    def customImage = docker.build(imageName)
                    customImage.push();
                }

                echo 'This will run only if successful'
                withCredentials([string(credentialsId: 'telegramToken' , variable: 'TOKEN')]) {
                    withCredentials([string(credentialsId: 'telegramChatid' , variable: 'CHAT_ID')]) {
                        sh "curl --location --request POST 'https://api.telegram.org/bot$TOKEN/sendMessage' --form text='$JOB_NAME docker build success' --form chat_id='$CHAT_ID'"
                    }           
                }
            }
        }
    } catch (e) {
        echo 'This will run only if failed'
        withCredentials([string(credentialsId: 'telegramToken' , variable: 'TOKEN')]) {
            withCredentials([string(credentialsId: 'telegramChatid' , variable: 'CHAT_ID')]) {
                sh "curl --location --request POST 'https://api.telegram.org/bot$TOKEN/sendMessage' --form text='$JOB_NAME docker build failed' --form chat_id='$CHAT_ID'"
            }           
        }

        throw e
    } finally {
        echo 'Docker build finished'
    }

    stage('Aprovisioning') {
         switch (env.BRANCH_NAME) {
            case 'main':
                sh "curl ${MAIN_WEBHOOKS_URL}/hooks/redeploy-icargo-backend-produccion"
                break;
            case 'testing':
                sh "curl ${TESTING_WEBHOOKS_URL}/hooks/redeploy-icargo-backend-testing"
                break;
            case 'develop':
                sh "curl ${DESARROLLO_WEBHOOKS_URL}/hooks/redeploy-icargo-backend-develop"
                break;
         }
    }

    stage('Final') {
        if (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'testing' || env.BRANCH_NAME == 'develop') {
            withCredentials([string(credentialsId: 'telegramToken' , variable: 'TOKEN')]) {
                withCredentials([string(credentialsId: 'telegramChatid' , variable: 'CHAT_ID')]) {
                    sh "curl --location --request POST 'https://api.telegram.org/bot$TOKEN/sendMessage' --form text='$JOB_NAME finished' --form chat_id='$CHAT_ID'"
                }       
            }
        }
    }
}