class MatchingManager {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.selectedZodiac1 = null;
        this.selectedZodiac2 = null;
        this.init();
    }

    init() {
        // 初始化星座选择网格
        this.initZodiacGrids();
        // 添加事件监听
        this.addEventListeners();
    }

    initZodiacGrids() {
        const zodiacData = [
            { id: 'aries', name: '白羊座', symbol: '♈' },
            { id: 'taurus', name: '金牛座', symbol: '♉' },
            { id: 'gemini', name: '双子座', symbol: '♊' },
            { id: 'cancer', name: '巨蟹座', symbol: '♋' },
            { id: 'leo', name: '狮子座', symbol: '♌' },
            { id: 'virgo', name: '处女座', symbol: '♍' },
            { id: 'libra', name: '天秤座', symbol: '♎' },
            { id: 'scorpio', name: '天蝎座', symbol: '♏' },
            { id: 'sagittarius', name: '射手座', symbol: '♐' },
            { id: 'capricorn', name: '摩羯座', symbol: '♑' },
            { id: 'aquarius', name: '水瓶座', symbol: '♒' },
            { id: 'pisces', name: '双鱼座', symbol: '♓' }
        ];

        // 生成两个选择网格
        ['yourZodiac', 'partnerZodiac'].forEach(gridId => {
            const grid = document.getElementById(gridId);
            if (!grid) return;

            grid.innerHTML = zodiacData.map(zodiac => `
                <div class="zodiac-item" data-zodiac="${zodiac.id}">
                    <div class="zodiac-icon">
                        <img src="../../images/zodiac/${zodiac.id}.png" 
                             alt="${zodiac.name}" 
                             onerror="this.src='../../images/zodiac/default.png'">
                        <span class="zodiac-symbol">${zodiac.symbol}</span>
                    </div>
                    <h4>${zodiac.name}</h4>
                </div>
            `).join('');
        });
    }

    addEventListeners() {
        // 添加星座选择事件
        document.querySelectorAll('#yourZodiac .zodiac-item').forEach(item => {
            item.addEventListener('click', () => this.selectZodiac(1, item));
        });

        document.querySelectorAll('#partnerZodiac .zodiac-item').forEach(item => {
            item.addEventListener('click', () => this.selectZodiac(2, item));
        });
    }

    selectZodiac(position, element) {
        // 移除同组其他选中状态
        const container = position === 1 ? '#yourZodiac' : '#partnerZodiac';
        document.querySelectorAll(`${container} .zodiac-item`).forEach(item => {
            item.classList.remove('selected');
        });

        // 添加选中状态
        element.classList.add('selected');

        // 保存选择
        const zodiacId = element.dataset.zodiac;
        if (position === 1) {
            this.selectedZodiac1 = zodiacId;
        } else {
            this.selectedZodiac2 = zodiacId;
        }

        // 如果两个星座都已选择，获取配对结果
        if (this.selectedZodiac1 && this.selectedZodiac2) {
            this.getCompatibility();
        }
    }

    async getCompatibility() {
        try {
            const response = await fetch(
                `${this.apiUrl}/compatibility/${this.selectedZodiac1}/${this.selectedZodiac2}`
            );
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            this.showResult(data);
        } catch (error) {
            console.error('Error getting compatibility:', error);
            // 可以添加错误提示
        }
    }

    showResult(data) {
        // 显示结果区域
        const resultSection = document.querySelector('.matching-result');
        resultSection.style.display = 'block';

        // 更新分数
        document.querySelector('.score').textContent = data.score;

        // 更新星座信息
        this.updateZodiacInfo('.zodiac1', data.zodiac1);
        this.updateZodiacInfo('.zodiac2', data.zodiac2);

        // 更新整体分析
        const overallAnalysis = document.querySelector('.overall-analysis');
        if (overallAnalysis) {
            overallAnalysis.textContent = data.analysis.overall || '暂无分析';
        }

        // 更新相处建议
        const relationshipAdvice = document.querySelector('.relationship-advice');
        if (relationshipAdvice) {
            relationshipAdvice.textContent = data.analysis.relationship || '暂无建议';
        }

        // 更新优势列表
        const advantageList = document.querySelector('.advantage-list');
        if (advantageList && data.analysis.advantages) {
            advantageList.innerHTML = data.analysis.advantages
                .map(adv => `<li>${adv}</li>`)
                .join('');
        }

        // 更新注意事项列表
        const disadvantageList = document.querySelector('.disadvantage-list');
        if (disadvantageList && data.analysis.disadvantages) {
            disadvantageList.innerHTML = data.analysis.disadvantages
                .map(dis => `<li>${dis}</li>`)
                .join('');
        }

        // 平滑滚动到结果区域
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    updateZodiacInfo(selector, data) {
        const container = document.querySelector(selector);
        if (!container) return;

        // 更新图片
        const img = container.querySelector('.zodiac-img');
        if (img) {
            img.src = `../../images/zodiac/${data.name}.png`;
            img.alt = data.name;
            img.onerror = () => {
                img.src = '../../images/zodiac/default.png';
            };
        }

        // 更新名称
        const name = container.querySelector('.zodiac-name');
        if (name) {
            name.textContent = data.name;
        }

        // 更新元素属性
        const element = container.querySelector('.zodiac-element');
        if (element) {
            element.textContent = data.element;
        }

        // 更新性格特点
        const traits = container.querySelector('.zodiac-traits');
        if (traits && data.personality) {
            traits.innerHTML = data.personality
                .map(trait => `<li>${trait}</li>`)
                .join('');
        }
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new MatchingManager();
}); 