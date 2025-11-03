
import streamlit as st
import os

def load_flip_counter_assets():
    """加载翻牌计数器的CSS和JS"""
    # 读取CSS文件
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'flip_counter.css')
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'flip_counter.js')
    
    css_content = ""
    js_content = ""
    
    try:
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
    except Exception as e:
        print(f"无法加载翻牌CSS: {e}")
    
    try:
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
    except Exception as e:
        print(f"无法加载翻牌JS: {e}")
    
    return css_content, js_content

def load_css():
    # 加载翻牌计数器资源
    flip_css, flip_js = load_flip_counter_assets()
    
    st.markdown(f"""
    <style>
        {flip_css}
        /* 全局样式 - 高级深色主题 */
        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
            color: #e2e8f0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* 按钮样式 - 现代渐变 */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.875rem 1.75rem;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: 0.025em;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.25);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px 0 rgba(99, 102, 241, 0.4);
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* 输入框样式 */
        .stSelectbox > div > div > select,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: rgba(30, 41, 59, 0.6);
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            transition: all 0.2s ease;
        }
        
        .stSelectbox > div > div > select:focus,
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* 主标题样式 - 精致渐变 */
        .main-header {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 2.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #6366f1);
            background-size: 200% 100%;
            animation: gradient 3s ease infinite;
        }
        
        @keyframes gradient {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .main-header h1 {
            margin: 0;
            font-size: 2.75rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.025em;
        }
        
        .main-header p {
            margin: 1rem 0 0 0;
            font-size: 1.125rem;
            opacity: 0.85;
            font-weight: 400;
            color: #cbd5e1;
        }
        
        /* 指标卡片样式 - 精致设计 */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.6) 100%);
            border-radius: 14px;
            padding: 1.75rem;
            margin: 0.75rem 0;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.15);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            border-color: rgba(148, 163, 184, 0.25);
        }
        
        .metric-card h3 {
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin: 0 0 0.75rem 0;
        }
        
        .metric-card h2 {
            font-size: 2rem;
            font-weight: 700;
            margin: 0.5rem 0;
            color: #f1f5f9;
        }
        
        .metric-card p {
            font-size: 0.9rem;
            color: #cbd5e1;
            margin: 0.5rem 0 0 0;
        }
        
        .metric-card small {
            font-size: 0.8rem;
            color: #94a3b8;
            display: block;
            margin-top: 0.5rem;
        }
        
        /* 状态颜色 - 优雅渐变 */
        .success-metric {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
            border-color: rgba(16, 185, 129, 0.3);
        }
        
        .success-metric h2, .success-metric h3 {
            color: #10b981;
        }
        
        .warning-metric {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
            border-color: rgba(245, 158, 11, 0.3);
        }
        
        .warning-metric h2, .warning-metric h3 {
            color: #f59e0b;
        }
        
        .danger-metric {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
            border-color: rgba(239, 68, 68, 0.3);
        }
        
        .danger-metric h2, .danger-metric h3 {
            color: #ef4444;
        }
        
        .info-metric {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.1) 100%);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        .info-metric h2, .info-metric h3 {
            color: #3b82f6;
        }
        
        /* 图表容器样式 - 现代卡片 */
        .chart-container {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(51, 65, 85, 0.4) 100%);
            border-radius: 14px;
            padding: 2rem;
            margin: 1.25rem 0;
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }
        
        .chart-container h4 {
            font-size: 1.125rem;
            font-weight: 600;
            color: #e2e8f0;
            margin: 0 0 1rem 0;
            letter-spacing: -0.01em;
        }
        
        .chart-container ul {
            list-style: none;
            padding: 0;
            margin: 1rem 0;
        }
        
        .chart-container li {
            padding: 0.5rem 0;
            color: #cbd5e1;
            line-height: 1.6;
        }
        
        .chart-container li::before {
            content: "▸";
            color: #6366f1;
            font-weight: bold;
            margin-right: 0.75rem;
        }
        
        /* 侧边栏样式 */
        .sidebar .sidebar-content {
            background: rgba(30, 41, 59, 0.4);
            border-radius: 12px;
            padding: 1.25rem;
            margin: 0.75rem 0;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        /* 密码字段样式 */
        input[type="password"] {
            background: rgba(30, 41, 59, 0.6) !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 10px !important;
        }
        
        /* Tab样式优化 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(30, 41, 59, 0.4);
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        }
        
        /* DataFrames样式 */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 1.875rem;
            }
            
            .main-header p {
                font-size: 0.95rem;
            }
            
            .metric-card {
                padding: 1.25rem;
            }
            
            .metric-card h2 {
                font-size: 1.5rem;
            }
            
            .chart-container {
                padding: 1.25rem;
            }
        }
        
        @media (max-width: 480px) {
            .main-header {
                padding: 1.5rem;
            }
            
            .main-header h1 {
                font-size: 1.5rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
            
            .stButton > button {
                padding: 0.625rem 1.25rem;
                font-size: 0.875rem;
            }
        }
        
        /* 滚动条样式 */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(30, 41, 59, 0.3);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.5);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.7);
        }
    </style>
    <script>
        {flip_js}
    </script>
    """, unsafe_allow_html=True)
