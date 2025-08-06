module.exports = {
  apps: [
    {
      name: 'jesse-plus-system',
      script: 'start_complete_system.py',
      cwd: '/root/Jesse+',
      interpreter: '/root/Jesse+/jesse_venv/bin/python',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '/root/Jesse+'
      },
      error_file: '/root/Jesse+/logs/err.log',
      out_file: '/root/Jesse+/logs/out.log',
      log_file: '/root/Jesse+/logs/combined.log',
      time: true
    }
  ]
}; 