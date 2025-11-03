/**
 * 机械翻牌计数器
 * 实现数字变化时的翻牌效果
 */

class FlipCounter {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            value: 0,
            decimals: 0,
            duration: 600,
            separator: '',
            prefix: '',
            suffix: '',
            theme: 'default', // default, success, warning, danger, info
            size: 'medium', // small, medium, large, xlarge
            ...options
        };
        
        this.currentValue = this.options.value;
        this.targetValue = this.options.value;
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        this.element.classList.add('flip-counter', this.options.size);
        if (this.options.theme !== 'default') {
            this.element.classList.add(this.options.theme);
        }
        this.render();
    }
    
    formatNumber(num) {
        const fixed = num.toFixed(this.options.decimals);
        return fixed.replace(/\B(?=(\d{3})+(?!\d))/g, this.options.separator);
    }
    
    render() {
        const formattedValue = this.formatNumber(this.currentValue);
        const fullValue = this.options.prefix + formattedValue + this.options.suffix;
        
        this.element.innerHTML = '';
        
        for (let i = 0; i < fullValue.length; i++) {
            const char = fullValue[i];
            
            if (/\d/.test(char)) {
                // 数字 - 创建翻牌
                const wrapper = document.createElement('span');
                wrapper.className = 'flip-digit-wrapper';
                
                const digit = document.createElement('span');
                digit.className = 'flip-digit';
                digit.dataset.value = char;
                
                const top = document.createElement('span');
                top.className = 'flip-digit-top';
                top.innerHTML = `<span>${char}</span>`;
                
                const bottom = document.createElement('span');
                bottom.className = 'flip-digit-bottom';
                bottom.innerHTML = `<span>${char}</span>`;
                
                digit.appendChild(top);
                digit.appendChild(bottom);
                wrapper.appendChild(digit);
                this.element.appendChild(wrapper);
            } else {
                // 非数字 - 直接显示
                const separator = document.createElement('span');
                separator.className = 'flip-separator';
                separator.textContent = char;
                this.element.appendChild(separator);
            }
        }
    }
    
    async flipDigit(digitElement, oldValue, newValue) {
        return new Promise((resolve) => {
            const top = digitElement.querySelector('.flip-digit-top span');
            const bottom = digitElement.querySelector('.flip-digit-bottom span');
            
            // 设置初始值
            top.textContent = oldValue;
            bottom.textContent = oldValue;
            
            // 开始翻牌动画
            digitElement.classList.add('flipping');
            
            // 动画中途更新底部数字
            setTimeout(() => {
                bottom.textContent = newValue;
            }, this.options.duration / 2);
            
            // 动画结束后更新顶部数字并移除动画类
            setTimeout(() => {
                top.textContent = newValue;
                digitElement.classList.remove('flipping');
                digitElement.dataset.value = newValue;
                resolve();
            }, this.options.duration);
        });
    }
    
    async updateValue(newValue) {
        if (this.isAnimating) return;
        
        this.targetValue = newValue;
        const oldFormatted = this.formatNumber(this.currentValue);
        const newFormatted = this.formatNumber(this.targetValue);
        
        // 如果格式化后的字符串长度不同，重新渲染
        if (oldFormatted.length !== newFormatted.length) {
            this.currentValue = this.targetValue;
            this.render();
            return;
        }
        
        this.isAnimating = true;
        const digits = this.element.querySelectorAll('.flip-digit');
        const promises = [];
        
        // 找出需要翻牌的数字
        for (let i = 0, digitIndex = 0; i < oldFormatted.length; i++) {
            if (/\d/.test(oldFormatted[i])) {
                const oldDigit = oldFormatted[i];
                const newDigit = newFormatted[i];
                
                if (oldDigit !== newDigit && digitIndex < digits.length) {
                    promises.push(
                        this.flipDigit(digits[digitIndex], oldDigit, newDigit)
                    );
                }
                digitIndex++;
            }
        }
        
        await Promise.all(promises);
        this.currentValue = this.targetValue;
        this.isAnimating = false;
    }
    
    setValue(value) {
        this.updateValue(value);
    }
    
    getValue() {
        return this.currentValue;
    }
    
    setTheme(theme) {
        this.element.classList.remove('success', 'warning', 'danger', 'info');
        if (theme !== 'default') {
            this.element.classList.add(theme);
        }
        this.options.theme = theme;
    }
    
    destroy() {
        this.element.innerHTML = '';
        this.element.classList.remove('flip-counter', this.options.size, this.options.theme);
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('[data-flip-counter]');
    counters.forEach(element => {
        const options = {
            value: parseFloat(element.dataset.value || 0),
            decimals: parseInt(element.dataset.decimals || 0),
            separator: element.dataset.separator || '',
            prefix: element.dataset.prefix || '',
            suffix: element.dataset.suffix || '',
            theme: element.dataset.theme || 'default',
            size: element.dataset.size || 'medium'
        };
        
        const counter = new FlipCounter(element, options);
        element.flipCounter = counter;
    });
});

// 导出到全局
window.FlipCounter = FlipCounter;
