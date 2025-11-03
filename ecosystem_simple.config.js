module.exports = {
  apps: [
    {
      name: 'jesse-plus-system',
      script: '/home/ubuntu/Jesse+/jesse_venv/bin/python',
      args: ['start_web_interface.py'],
      cwd: '/home/ubuntu/Jesse+',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      max_restarts: 3,
      min_uptime: '10s',
      env: {
        PORT: 8060,
        PYTHONPATH: '/home/ubuntu/Jesse+'
      }
    },
    {
      name: 'jesse-auto-evolution', 
      script: '/home/ubuntu/Jesse+/jesse_venv/bin/python',
      args: ['start_auto_evolution_system.py'],
      cwd: '/home/ubuntu/Jesse+',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      max_restarts: 3,
      min_uptime: '10s',
      env: {
        PYTHONPATH: '/home/ubuntu/Jesse+'
      }
    },
    {
      name: 'jesse-trading-system',
      script: '/home/ubuntu/Jesse+/jesse_venv/bin/python', 
      args: ['run_high_frequency_trading.py'],
      cwd: '/home/ubuntu/Jesse+',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      max_restarts: 3,
      min_uptime: '10s',
      env: {
        PYTHONPATH: '/home/ubuntu/Jesse+'
      }
    }
  ]
};
