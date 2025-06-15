class HoroscopeManager {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.currentZodiac = this.getZodiacFromUrl() || 'aries';
        this.currentPeriod = 'daily';
        this.init();
    }

    init() {
        // 初始化星座选择器
        this.initZodiacSelector();
        // 初始化标签页切换
        this.initTabs();
        // 加载星座基本信息
        this.loadZodiacInfo();
        // 加载运势信息
        this.loadHoroscope();
    }

    // 添加星座选择器初始化
    initZodiacSelector() {
        const selector = document.getElementById('zodiacSelect');
        if (selector) {
            // 设置当前选中的星座
            selector.value = this.currentZodiac;
            // 添加选择事件监听
            selector.addEventListener('change', async (e) => {
                this.currentZodiac = e.target.value;
                
                // 更新图片
                const zodiacImage = document.querySelector('.zodiac-image');
                if (zodiacImage) {
                    zodiacImage.src = `../../images/zodiac/${this.currentZodiac}.png`;
                    zodiacImage.alt = this.getZodiacName(this.currentZodiac);
                }

                // 更新 URL
                const url = new URL(window.location.href);
                url.searchParams.set('zodiac', this.currentZodiac);
                window.history.pushState({}, '', url);

                // 重新加载数据
                await this.loadZodiacInfo();
                await this.loadHoroscope();
            });
        }
    }

    // 从 URL 获取星座参数
    getZodiacFromUrl() {
        const params = new URLSearchParams(window.location.search);
        return params.get('zodiac');
    }

    // 添加获取星座中文名的方法
    getZodiacName(zodiac) {
        const names = {
            aries: '白羊座',
            taurus: '金牛座',
            gemini: '双子座',
            cancer: '巨蟹座',
            leo: '狮子座',
            virgo: '处女座',
            libra: '天秤座',
            scorpio: '天蝎座',
            sagittarius: '射手座',
            capricorn: '摩羯座',
            aquarius: '水瓶座',
            pisces: '双鱼座'
        };
        return names[zodiac] || zodiac;
    }

    initTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // 移除所有活动状态
                tabButtons.forEach(btn => btn.classList.remove('active'));
                // 设置当前标签为活动状态
                button.classList.add('active');
                // 更新当前周期
                this.currentPeriod = button.dataset.tab;
                // 加载对应运势
                this.loadHoroscope();
            });
        });
    }

    async loadZodiacInfo() {
        try {
            const response = await fetch(`${this.apiUrl}/zodiac/${this.currentZodiac}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            // 立即更新页面内容
            this.updateZodiacInfo(data);
            
            // 更新页面标题
            document.title = `${this.getZodiacName(this.currentZodiac)} - 星座运势详情`;
        } catch (error) {
            console.error('Error loading zodiac info:', error);
        }
    }

    async loadHoroscope() {
        try {
            const response = await fetch(`${this.apiUrl}/horoscope/${this.currentZodiac}/${this.currentPeriod}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            this.updateHoroscope(data);
        } catch (error) {
            console.error('Error loading horoscope:', error);
            // 可以添加错误提示UI
        }
    }

    updateZodiacInfo(data) {
        // 更新基本信息
        document.querySelector('.zodiac-name').textContent = data.name;
        document.querySelector('.date-range').textContent = data.date_range;
        document.querySelector('.element').textContent = data.element;
        document.querySelector('.ruling-planet').textContent = `守护星：${data.ruling_planet}`;
        document.querySelector('.zodiac-symbol').textContent = this.getZodiacSymbol(this.currentZodiac);

        // 更新性格特点
        const traitsList = document.querySelector('.traits-list');
        traitsList.innerHTML = data.personality
            .map(trait => `<li>${trait}</li>`)
            .join('');

        // 更新优点
        const strengthsList = document.querySelector('.strengths ul');
        strengthsList.innerHTML = data.strengths
            .map(strength => `<li>${strength}</li>`)
            .join('');

        // 更新缺点
        const weaknessesList = document.querySelector('.weaknesses ul');
        weaknessesList.innerHTML = data.weaknesses
            .map(weakness => `<li>${weakness}</li>`)
            .join('');
    }

    updateHoroscope(data) {
        // 更新标题和日期信息
        const periodTitles = {
            'daily': '今日运势概览',
            'weekly': '本周运势概览',
            'monthly': '本月运势概览',
            'yearly': '年度运势概览'
        };
        
        document.querySelector('.fortune-card h3').textContent = periodTitles[this.currentPeriod];
        document.querySelector('.fortune-date').textContent = data.period.date;

        // 清空现有运势项目
        const fortuneItems = document.querySelector('.fortune-items');
        fortuneItems.innerHTML = '';

        // 添加运势项目
        const items = {
            overall: '综合运势',
            love: '感情运势',
            career: '事业运势',
            wealth: '财运',
            health: '健康运势'
        };

        Object.entries(items).forEach(([key, title]) => {
            const itemHtml = `
                <div class="fortune-item">
                    <h4>${title}</h4>
                    <div class="stars">${data[key]}</div>
                    <p class="fortune-desc">${data.description[key]}</p>
                </div>
            `;
            fortuneItems.insertAdjacentHTML('beforeend', itemHtml);
        });
    }

    getZodiacSymbol(zodiac) {
        const symbols = {
            aries: '♈',
            taurus: '♉',
            gemini: '♊',
            cancer: '♋',
            leo: '♌',
            virgo: '♍',
            libra: '♎',
            scorpio: '♏',
            sagittarius: '♐',
            capricorn: '♑',
            aquarius: '♒',
            pisces: '♓'
        };
        return symbols[zodiac] || '★';
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new HoroscopeManager();
}); 