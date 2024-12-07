// 用户认证相关功能
class UserAuth {
    constructor() {
        this.form = document.querySelector('.auth-form');
        this.apiUrl = 'http://localhost:5000/api';
        this.init();
    }

    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
        
        // 添加输入验证
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', () => {
                this.validatePasswords(passwordInput, confirmPasswordInput);
            });
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries());

        // 判断是登录还是注册表单
        if (this.form.id === 'loginForm') {
            this.login(data);
        } else if (this.form.id === 'registerForm') {
            this.register(data);
        }
    }

    async login(data) {
        try {
            const response = await fetch(`${this.apiUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error);
            }

            // 保存用户信息到 localStorage
            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));

            alert('登录成功！');
            
            // 设置一个标记，表示需要刷新页面
            localStorage.setItem('needRefresh', 'true');
            
            // 跳转到首页
            window.location.href = '../../';
        } catch (error) {
            console.error('Login error:', error);
            this.showError(error.message);
        }
    }

    async register(data) {
        try {
            if (data.password !== data.confirmPassword) {
                this.showError('两次输入的密码不一致');
                return;
            }

            const response = await fetch(`${this.apiUrl}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error);
            }

            alert('注册成功！');
            window.location.href = 'login.html';
        } catch (error) {
            this.showError(error.message);
        }
    }

    validatePasswords(password1, password2) {
        if (password2.value && password1.value !== password2.value) {
            password2.setCustomValidity('密码不匹配');
        } else {
            password2.setCustomValidity('');
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;

        // 移除之前的错误消息
        const existingError = this.form.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        this.form.insertBefore(errorDiv, this.form.firstChild);
    }
}

// 初始化用户认证功能
new UserAuth(); 