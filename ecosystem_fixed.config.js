module.exports = {
  apps: [
    {
      name: 'jesse-plus-system',
      script: 'start_web_interface.py',
      cwd: '/home/ubuntu/Jesse+',
      interpreter: '/home/ubuntu/Jesse+/jesse_venv/bin/python',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8060,
        PYTHONPATH: '/home/ubuntu/Jesse+'
      },
      error_file: '/home/ubuntu/Jesse+/logs/web_interface_error.log',
      out_file: '/home/ubuntu/Jesse+/logs/web_interface_out.log',
      log_file: '/home/ubuntu/Jesse+/logs/web_interface_combined.log',
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_restarts: 5,
      min_uptime: '30s',
      restart_delay: 2000
    },
    {
      name: 'jesse-auto-evolution',
      script: 'start_auto_evolution_system.py',
      interpreter: '/home/ubuntu/Jesse+/jesse_venv/bin/python',
      cwd: '/home/ubuntu/Jesse+',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '/home/ubuntu/Jesse+'
      },
      error_file: '/home/ubuntu/Jesse+/logs/auto_evolution_error.log',
      out_file: '/home/ubuntu/Jesse+/logs/auto_evolution_out.log',
      log_file: '/home/ubuntu/Jesse+/logs/auto_evolution_combined.log',
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_restarts: 5,
      min_uptime: '30s',
      restart_delay: 2000
    },
    {
      name: 'jesse-trading-system',
      script: 'run_high_frequency_trading.py',
      interpreter: '/home/ubuntu/Jesse+/jesse_venv/bin/python',
      cwd: '/home/ubuntu/Jesse+',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '/home/ubuntu/Jesse+'
      },
      error_file: '/home/ubuntu/Jesse+/logs/trading_error.log',
      out_file: '/home/ubuntu/Jesse+/logs/trading_out.log',
      log_file: '/home/ubuntu/Jesse+/logs/trading_combined.log',
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_restarts: 5,
      min_uptime: '30s',
      restart_delay: 2000
    }
  ]
};
