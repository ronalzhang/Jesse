"""
AI增强器
整合所有AI功能，提供统一的AI增强接口
"""

import logging
from typing import Dict, List, Any
import numpy as np
import pandas as pd

from .market_analyzer import MarketAnalyzer
from .strategy_evolver import StrategyEvolver
from .price_predictor import PricePredictor

class AIEnhancer:
    """AI增强器主类"""
    
    def __init__(self):
        """初始化AI增强器"""
        self.logger = logging.getLogger(__name__)
        
        # 初始化AI组件
        self.market_analyzer = MarketAnalyzer()
        self.strategy_evolver = StrategyEvolver()
        self.price_predictor = PricePredictor()
        
        self.is_initialized = False
        
    def initialize(self):
        """初始化AI增强器"""
        try:
            self.logger.info("🤖 初始化AI增强器...")
            
            # 初始化各个AI组件
            self.market_analyzer.initialize()
            self.strategy_evolver.initialize()
            self.price_predictor.initialize()
            
            self.is_initialized = True
            self.logger.info("✅ AI增强器初始化完成")
            
        except Exception as e:
            self.logger.error(f"❌ AI增强器初始化失败: {e}")
            raise
    
    def analyze_market(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI驱动的市场分析"""
        try:
            self.logger.info("🧠 开始AI市场分析...")
            
            # 1. 市场情绪分析
            sentiment_analysis = self.market_analyzer.analyze_sentiment(market_data)
            
            # 2. 技术指标分析
            technical_analysis = self.market_analyzer.analyze_technical_indicators(market_data)
            
            # 3. 价格预测
            price_predictions = self.price_predictor.predict_prices(market_data)
            
            # 4. 市场趋势分析
            trend_analysis = self.market_analyzer.analyze_trends(market_data)
            
            # 5. 综合市场分析
            comprehensive_analysis = {
                'sentiment': sentiment_analysis,
                'technical': technical_analysis,
                'predictions': price_predictions,
                'trends': trend_analysis,
                'timestamp': pd.Timestamp.now(),
                'confidence': self._calculate_overall_confidence(
                    sentiment_analysis, technical_analysis, price_predictions
                )
            }
            
            self.logger.info("✅ AI市场分析完成")
            return comprehensive_analysis
            
        except Exception as e:
            self.logger.error(f"❌ AI市场分析失败: {e}")
            return {'error': str(e)}
    
    def evolve_strategies(self, market_data: Dict[str, Any], 
                         ai_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI驱动的策略进化"""
        try:
            self.logger.info("🧬 开始AI策略进化...")
            
            # 1. 基于市场分析进化策略
            evolved_strategies = self.strategy_evolver.evolve_strategies(
                market_data, ai_analysis
            )
            
            # 2. 优化策略参数
            optimized_strategies = self.strategy_evolver.optimize_parameters(
                evolved_strategies, ai_analysis
            )
            
            # 3. 策略性能评估
            evaluated_strategies = self.strategy_evolver.evaluate_strategies(
                optimized_strategies, market_data
            )
            
            # 4. 选择最佳策略
            best_strategies = self.strategy_evolver.select_best_strategies(
                evaluated_strategies, top_k=5
            )
            
            self.logger.info(f"✅ AI策略进化完成，生成了 {len(best_strategies)} 个最佳策略")
            return best_strategies
            
        except Exception as e:
            self.logger.error(f"❌ AI策略进化失败: {e}")
            return []
    
    def get_trading_signals(self, market_data: Dict[str, Any], 
                           ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """获取AI驱动的交易信号"""
        try:
            self.logger.info("📡 生成AI交易信号...")
            
            # 1. 综合分析生成信号
            sentiment_signal = self._generate_sentiment_signal(ai_analysis['sentiment'])
            technical_signal = self._generate_technical_signal(ai_analysis['technical'])
            prediction_signal = self._generate_prediction_signal(ai_analysis['predictions'])
            
            # 2. 信号融合
            combined_signal = self._combine_signals([
                sentiment_signal, technical_signal, prediction_signal
            ])
            
            # 3. 风险评估
            risk_assessment = self._assess_risk(market_data, combined_signal)
            
            # 4. 最终交易决策
            final_decision = self._make_final_decision(combined_signal, risk_assessment)
            
            trading_signals = {
                'sentiment_signal': sentiment_signal,
                'technical_signal': technical_signal,
                'prediction_signal': prediction_signal,
                'combined_signal': combined_signal,
                'risk_assessment': risk_assessment,
                'final_decision': final_decision,
                'timestamp': pd.Timestamp.now()
            }
            
            self.logger.info("✅ AI交易信号生成完成")
            return trading_signals
            
        except Exception as e:
            self.logger.error(f"❌ AI交易信号生成失败: {e}")
            return {'error': str(e)}
    
    def _calculate_overall_confidence(self, sentiment: Dict, technical: Dict, 
                                    predictions: Dict) -> float:
        """计算整体置信度"""
        try:
            # 加权平均计算整体置信度
            sentiment_conf = sentiment.get('confidence', 0.5)
            technical_conf = technical.get('confidence', 0.5)
            prediction_conf = predictions.get('confidence', 0.5)
            
            # 权重设置
            weights = [0.3, 0.4, 0.3]  # 技术分析权重最高
            
            overall_confidence = (
                sentiment_conf * weights[0] +
                technical_conf * weights[1] +
                prediction_conf * weights[2]
            )
            
            return min(max(overall_confidence, 0.0), 1.0)  # 限制在0-1之间
            
        except Exception as e:
            self.logger.error(f"❌ 计算整体置信度失败: {e}")
            return 0.5
    
    def _generate_sentiment_signal(self, sentiment_analysis: Dict) -> Dict[str, Any]:
        """基于情绪分析生成交易信号"""
        try:
            sentiment_score = sentiment_analysis.get('overall_sentiment', 0.0)
            
            if sentiment_score > 0.6:
                signal = 'buy'
                confidence = sentiment_score
            elif sentiment_score < 0.4:
                signal = 'sell'
                confidence = 1.0 - sentiment_score
            else:
                signal = 'hold'
                confidence = 0.5
            
            return {
                'signal': signal,
                'confidence': confidence,
                'sentiment_score': sentiment_score,
                'reasoning': f'基于情绪分析，市场情绪评分为{sentiment_score:.2f}'
            }
            
        except Exception as e:
            self.logger.error(f"❌ 生成情绪信号失败: {e}")
            return {'signal': 'hold', 'confidence': 0.5, 'error': str(e)}
    
    def _generate_technical_signal(self, technical_analysis: Dict) -> Dict[str, Any]:
        """基于技术分析生成交易信号"""
        try:
            # 获取技术指标
            rsi = technical_analysis.get('rsi', 50)
            macd = technical_analysis.get('macd_signal', 'neutral')
            ma_trend = technical_analysis.get('ma_trend', 'neutral')
            
            # 综合技术信号
            signals = []
            confidences = []
            
            # RSI信号
            if rsi < 30:
                signals.append('buy')
                confidences.append(0.8)
            elif rsi > 70:
                signals.append('sell')
                confidences.append(0.8)
            else:
                signals.append('hold')
                confidences.append(0.5)
            
            # MACD信号
            if macd == 'bullish':
                signals.append('buy')
                confidences.append(0.7)
            elif macd == 'bearish':
                signals.append('sell')
                confidences.append(0.7)
            else:
                signals.append('hold')
                confidences.append(0.5)
            
            # 均线趋势信号
            if ma_trend == 'bullish':
                signals.append('buy')
                confidences.append(0.6)
            elif ma_trend == 'bearish':
                signals.append('sell')
                confidences.append(0.6)
            else:
                signals.append('hold')
                confidences.append(0.5)
            
            # 综合决策
            buy_count = signals.count('buy')
            sell_count = signals.count('sell')
            hold_count = signals.count('hold')
            
            if buy_count > sell_count and buy_count > hold_count:
                final_signal = 'buy'
                confidence = np.mean([c for s, c in zip(signals, confidences) if s == 'buy'])
            elif sell_count > buy_count and sell_count > hold_count:
                final_signal = 'sell'
                confidence = np.mean([c for s, c in zip(signals, confidences) if s == 'sell'])
            else:
                final_signal = 'hold'
                confidence = np.mean(confidences)
            
            return {
                'signal': final_signal,
                'confidence': confidence,
                'technical_indicators': {
                    'rsi': rsi,
                    'macd': macd,
                    'ma_trend': ma_trend
                },
                'reasoning': f'技术分析显示：RSI={rsi:.1f}, MACD={macd}, 均线趋势={ma_trend}'
            }
            
        except Exception as e:
            self.logger.error(f"❌ 生成技术信号失败: {e}")
            return {'signal': 'hold', 'confidence': 0.5, 'error': str(e)}
    
    def _generate_prediction_signal(self, predictions: Dict) -> Dict[str, Any]:
        """基于价格预测生成交易信号"""
        try:
            price_prediction = predictions.get('price_prediction', {})
            current_price = price_prediction.get('current_price', 0)
            predicted_price = price_prediction.get('predicted_price', 0)
            confidence = price_prediction.get('confidence', 0.5)
            
            if current_price == 0 or predicted_price == 0:
                return {'signal': 'hold', 'confidence': 0.5, 'reasoning': '价格数据不足'}
            
            # 计算价格变化百分比
            price_change_pct = (predicted_price - current_price) / current_price
            
            # 根据预测变化生成信号
            if price_change_pct > 0.02:  # 预测上涨超过2%
                signal = 'buy'
                signal_confidence = confidence * min(abs(price_change_pct) * 10, 1.0)
            elif price_change_pct < -0.02:  # 预测下跌超过2%
                signal = 'sell'
                signal_confidence = confidence * min(abs(price_change_pct) * 10, 1.0)
            else:
                signal = 'hold'
                signal_confidence = confidence
            
            return {
                'signal': signal,
                'confidence': signal_confidence,
                'price_change_pct': price_change_pct,
                'current_price': current_price,
                'predicted_price': predicted_price,
                'reasoning': f'预测价格变化{price_change_pct:.2%}，当前价格{current_price}，预测价格{predicted_price}'
            }
            
        except Exception as e:
            self.logger.error(f"❌ 生成预测信号失败: {e}")
            return {'signal': 'hold', 'confidence': 0.5, 'error': str(e)}
    
    def _combine_signals(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """融合多个交易信号"""
        try:
            # 统计信号
            signal_counts = {'buy': 0, 'sell': 0, 'hold': 0}
            total_confidence = 0
            total_weight = 0
            
            for i, signal in enumerate(signals):
                signal_type = signal.get('signal', 'hold')
                confidence = signal.get('confidence', 0.5)
                
                signal_counts[signal_type] += 1
                total_confidence += confidence * (i + 1)  # 权重递增
                total_weight += (i + 1)
            
            # 确定最终信号
            if signal_counts['buy'] > signal_counts['sell'] and signal_counts['buy'] > signal_counts['hold']:
                final_signal = 'buy'
            elif signal_counts['sell'] > signal_counts['buy'] and signal_counts['sell'] > signal_counts['hold']:
                final_signal = 'sell'
            else:
                final_signal = 'hold'
            
            # 计算综合置信度
            avg_confidence = total_confidence / total_weight if total_weight > 0 else 0.5
            
            return {
                'signal': final_signal,
                'confidence': avg_confidence,
                'signal_counts': signal_counts,
                'reasoning': f'综合信号：买入{signal_counts["buy"]}次，卖出{signal_counts["sell"]}次，持有{signal_counts["hold"]}次'
            }
            
        except Exception as e:
            self.logger.error(f"❌ 融合信号失败: {e}")
            return {'signal': 'hold', 'confidence': 0.5, 'error': str(e)}
    
    def _assess_risk(self, market_data: Dict[str, Any], 
                    combined_signal: Dict[str, Any]) -> Dict[str, Any]:
        """风险评估"""
        try:
            # 简单的风险评估逻辑
            volatility = self._calculate_volatility(market_data)
            signal_confidence = combined_signal.get('confidence', 0.5)
            
            # 风险评分 (0-1，0为低风险，1为高风险)
            risk_score = (1 - signal_confidence) * 0.5 + volatility * 0.5
            
            risk_level = 'low' if risk_score < 0.3 else 'medium' if risk_score < 0.7 else 'high'
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'volatility': volatility,
                'recommendation': self._get_risk_recommendation(risk_level, combined_signal['signal'])
            }
            
        except Exception as e:
            self.logger.error(f"❌ 风险评估失败: {e}")
            return {'risk_score': 0.5, 'risk_level': 'medium', 'error': str(e)}
    
    def _calculate_volatility(self, market_data: Dict[str, Any]) -> float:
        """计算市场波动率"""
        try:
            # 简化的波动率计算
            all_prices = []
            for exchange_data in market_data.values():
                if 'ohlcv' in exchange_data:
                    ohlcv = exchange_data['ohlcv']
                    if ohlcv and len(ohlcv) > 1:
                        prices = [candle[4] for candle in ohlcv]  # 收盘价
                        all_prices.extend(prices)
            
            if len(all_prices) > 1:
                returns = np.diff(all_prices) / all_prices[:-1]
                volatility = np.std(returns)
                return min(volatility, 1.0)  # 限制在0-1之间
            else:
                return 0.5  # 默认中等波动率
                
        except Exception as e:
            self.logger.error(f"❌ 计算波动率失败: {e}")
            return 0.5
    
    def _get_risk_recommendation(self, risk_level: str, signal: str) -> str:
        """获取风险建议"""
        if risk_level == 'high':
            if signal == 'buy':
                return '高风险买入，建议小仓位或等待'
            elif signal == 'sell':
                return '高风险卖出，建议谨慎操作'
            else:
                return '高风险环境，建议观望'
        elif risk_level == 'medium':
            if signal == 'buy':
                return '中等风险买入，建议正常仓位'
            elif signal == 'sell':
                return '中等风险卖出，建议正常操作'
            else:
                return '中等风险环境，可以适度参与'
        else:  # low risk
            if signal == 'buy':
                return '低风险买入，可以适当加仓'
            elif signal == 'sell':
                return '低风险卖出，可以正常操作'
            else:
                return '低风险环境，适合稳健操作'
    
    def _make_final_decision(self, combined_signal: Dict[str, Any], 
                            risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """做出最终交易决策"""
        try:
            signal = combined_signal.get('signal', 'hold')
            confidence = combined_signal.get('confidence', 0.5)
            risk_score = risk_assessment.get('risk_score', 0.5)
            
            # 根据风险和置信度调整决策
            if risk_score > 0.7:  # 高风险
                if signal == 'buy':
                    final_signal = 'hold'  # 高风险时避免买入
                    adjusted_confidence = confidence * 0.5
                elif signal == 'sell':
                    final_signal = 'sell'  # 高风险时允许卖出
                    adjusted_confidence = confidence * 0.8
                else:
                    final_signal = 'hold'
                    adjusted_confidence = confidence
            else:  # 中低风险
                final_signal = signal
                adjusted_confidence = confidence
            
            return {
                'action': final_signal,
                'confidence': adjusted_confidence,
                'risk_score': risk_score,
                'reasoning': f'最终决策：{final_signal}，置信度{adjusted_confidence:.2f}，风险评分{risk_score:.2f}',
                'timestamp': pd.Timestamp.now()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 最终决策失败: {e}")
            return {'action': 'hold', 'confidence': 0.5, 'error': str(e)}
    
    def cleanup(self):
        """清理AI增强器资源"""
        try:
            self.logger.info("🧹 清理AI增强器资源...")
            
            # 清理各个AI组件
            self.market_analyzer.cleanup()
            self.strategy_evolver.cleanup()
            self.price_predictor.cleanup()
            
            self.logger.info("✅ AI增强器清理完成")
            
        except Exception as e:
            self.logger.error(f"❌ AI增强器清理失败: {e}") 