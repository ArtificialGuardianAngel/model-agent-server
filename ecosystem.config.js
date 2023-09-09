module.exports = {
    apps: [
        {
            name: 'layer',
            cmd: 'main.py',
            interpreter: '/home/loliallen/miniconda3/envs/model-layer/bin/python',
            instances: 2
        },
        {
            name: 'notification-system',
            script: './notification_system/build/index.js'
        }
    ],
}