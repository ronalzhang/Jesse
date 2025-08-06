module.exports = {
  apps: [
    {
      name: 'jesse-auto-evolution',
      script: 'start_auto_evolution_system.py',
      interpreter: 'python3',
      cwd: '/root/Jesse+',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8060
      },
      error_file: './logs/auto_evolution_error.log',
      out_file: './logs/auto_evolution_out.log',
      log_file: './logs/auto_evolution_combined.log',
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 4000,
      kill_timeout: 5000,
      wait_ready: true,
      listen_timeout: 8000
    },
    {
      name: 'jesse-trading-system',
      script: 'run_high_frequency_trading.py',
      interpreter: 'python3',
      cwd: '/root/Jesse+',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production'
      },
      error_file: './logs/trading_error.log',
      out_file: './logs/trading_out.log',
      log_file: './logs/trading_combined.log',
      time: true,
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 4000,
      kill_timeout: 5000,
      wait_ready: true,
      listen_timeout: 8000
    }
  ]
}; 