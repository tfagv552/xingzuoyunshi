// 轮播图数据
const sliderData = [
    {
        id: 1,
        image: 'images/slider/slide1.jpg',
        defaultImage: 'images/slider/default.jpg',
        title: '今日星座运势',
        description: '了解12星座今日运势详情'
    },
    {
        id: 2,
        image: 'images/slider/slide2.jpg',
        defaultImage: 'images/slider/default.jpg',
        title: '星座配对指南',
        description: '探索你的星座匹配对象'
    },
    {
        id: 3,
        image: 'images/slider/slide3.jpg',
        defaultImage: 'images/slider/default.jpg',
        title: '本周星座精选',
        description: '查看本周最旺星座排行'
    }
];

// 轮播图功能实现
class Slider {
    constructor() {
        this.container = document.querySelector('.slider-container');
        this.currentIndex = 0;
        this.init();
    }

    init() {
        // 创建轮播图结构
        this.createSlider();
        // 自动播放
        this.autoPlay();
        // 添加控制按钮
        this.addControls();
    }

    createSlider() {
        // 创建轮播图HTML结构
        const sliderHTML = `
            <div class="slider-wrapper">
                ${sliderData.map(slide => `
                    <div class="slide">
                        <img src="${slide.image}" alt="${slide.title}" 
                             onerror="this.onerror=null; this.src='${slide.defaultImage}';">
                        <div class="slide-content">
                            <h3>${slide.title}</h3>
                            <p>${slide.description}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
            <div class="slider-indicators">
                ${sliderData.map((_, index) => `
                    <span class="indicator${index === 0 ? ' active' : ''}" data-index="${index}"></span>
                `).join('')}
            </div>
        `;
        this.container.innerHTML = sliderHTML;
        this.wrapper = this.container.querySelector('.slider-wrapper');
        this.indicators = this.container.querySelectorAll('.indicator');
    }

    autoPlay() {
        setInterval(() => {
            this.next();
        }, 5000);
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % sliderData.length;
        this.updateSlider();
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + sliderData.length) % sliderData.length;
        this.updateSlider();
    }

    updateSlider() {
        this.wrapper.style.transform = `translateX(-${this.currentIndex * 100}%)`;
        // 更新指示器
        this.indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === this.currentIndex);
        });
    }

    addControls() {
        // 添加前后按钮
        const prevButton = document.createElement('button');
        const nextButton = document.createElement('button');
        prevButton.className = 'slider-control prev';
        nextButton.className = 'slider-control next';
        prevButton.innerHTML = '&lt;';
        nextButton.innerHTML = '&gt;';
        
        this.container.appendChild(prevButton);
        this.container.appendChild(nextButton);

        // 添加事件监听
        prevButton.addEventListener('click', () => this.prev());
        nextButton.addEventListener('click', () => this.next());
        
        // 指示器点击事件
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                this.currentIndex = index;
                this.updateSlider();
            });
        });
    }
}

// 初始化轮播图
new Slider();

// 在文件末尾添加用户状态管理代码
class UserManager {
    constructor() {
        this.guestActions = document.getElementById('guestActions');
        this.userProfile = document.getElementById('userProfile');
        this.init();
    }

    init() {
        // 添加退出登录事件监听
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    }

    logout() {
        // 清除用户数据
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        
        // 刷新页面
        window.location.reload();
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new Slider();
    new UserManager();
}); 