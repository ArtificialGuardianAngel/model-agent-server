import dotenv from 'dotenv'

dotenv.config()

export default {
    slackApiKey: process.env['SLACK_API_KEY'],
    port: process.env['PORT'] || 4444
}