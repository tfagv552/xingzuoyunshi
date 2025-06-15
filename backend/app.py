from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import jwt
import datetime
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # 允许跨域请求
app.config['SECRET_KEY'] = 'your-secret-key'  # 用于JWT加密

# 数据库初始化
def init_db():
    conn = sqlite3.connect('zodiac.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            birthdate TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 用户注册
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    try:
        conn = sqlite3.connect('zodiac.db')
        c = conn.cursor()
        
        # 检查用户名是否已存在
        c.execute('SELECT id FROM users WHERE username = ?', (data['username'],))
        if c.fetchone() is not None:
            return jsonify({'error': '用户名已存在'}), 400
        
        # 检查邮箱是否已存在
        c.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
        if c.fetchone() is not None:
            return jsonify({'error': '邮箱已被注册'}), 400
        
        # 创建新用户
        hashed_password = generate_password_hash(data['password'])
        c.execute('''
            INSERT INTO users (username, password, email, birthdate)
            VALUES (?, ?, ?, ?)
        ''', (data['username'], hashed_password, data['email'], data['birthdate']))
        
        conn.commit()
        return jsonify({'message': '注册成功'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    try:
        conn = sqlite3.connect('zodiac.db')
        c = conn.cursor()
        
        # 查找用户
        c.execute('SELECT * FROM users WHERE username = ?', (data['username'],))
        user = c.fetchone()
        
        if user is None:
            return jsonify({'error': '用户不存在'}), 404
        
        if not check_password_hash(user[2], data['password']):
            return jsonify({'error': '密码错误'}), 401
        
        # 生成 JWT token
        token = jwt.encode({
            'user_id': user[0],
            'username': user[1],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[3]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# 添加星座基础数据
ZODIAC_DATA = {
    'aries': {
        'name': '白羊座',
        'date_range': '3月21日 - 4月19日',
        'element': '火象星座',
        'ruling_planet': '火星',
        'symbol': '白羊',
        'personality': [
            '充满活力',
            '勇敢无畏',
            '直率坦白',
            '乐观向上',
            '富有冒险精神'
        ],
        'strengths': ['领导力', '勇气', '热情', '决断力'],
        'weaknesses': ['冲动', '固执', '急躁', '自我中心']
    },
    'taurus': {
        'name': '金牛座',
        'date_range': '4月20日 - 5月20日',
        'element': '土象星座',
        'ruling_planet': '金星',
        'symbol': '金牛',
        'personality': [
            '稳重踏实',
            '意志坚定',
            '重视物质',
            '享受生活',
            '注重实际'
        ],
        'strengths': ['耐心', '可靠', '坚韧', '务实'],
        'weaknesses': ['固执', '贪婪', '懒惰', '占有欲强']
    },
    'gemini': {
        'name': '双子座',
        'date_range': '5月21日 - 6月21日',
        'element': '风象星座',
        'ruling_planet': '水星',
        'symbol': '双子',
        'personality': [
            '聪明机智',
            '善于交际',
            '思维活跃',
            '适应能力强',
            '好奇心强'
        ],
        'strengths': ['交际能力', '学习能力', '灵活性', '表达能力'],
        'weaknesses': ['善变', '浮躁', '分散注意力', '优柔寡断']
    },
    'cancer': {
        'name': '巨蟹座',
        'date_range': '6月22日 - 7月22日',
        'element': '水象星座',
        'ruling_planet': '月亮',
        'symbol': '巨蟹',
        'personality': [
            '重情重义',
            '富有同情心',
            '保护欲强',
            '记忆力好',
            '重视家庭'
        ],
        'strengths': ['同理心', '保护能力', '记忆力', '创造力'],
        'weaknesses': ['敏感', '多愁善感', '依赖性强', '情绪化']
    },
    'leo': {
        'name': '狮子座',
        'date_range': '7月23日 - 8月22日',
        'element': '火象星座',
        'ruling_planet': '太阳',
        'symbol': '狮子',
        'personality': [
            '自信阳光',
            '慷慨大方',
            '领导才能',
            '创造力强',
            '重视荣誉'
        ],
        'strengths': ['领导力', '创造力', '自信心', '组织能力'],
        'weaknesses': ['自负', '专制', '好面子', '固执']
    },
    'virgo': {
        'name': '处女座',
        'date_range': '8月23日 - 9月22日',
        'element': '土象星座',
        'ruling_planet': '水星',
        'symbol': '处女',
        'personality': [
            '完美主义',
            '细心谨慎',
            '理性务实',
            '勤劳善良',
            '追求完美'
        ],
        'strengths': ['分析能力', '条理性', '责任心', '执行力'],
        'weaknesses': ['挑剔', '焦虑', '过分完美', '保守']
    },
    'libra': {
        'name': '天秤座',
        'date_range': '9月23日 - 10月23日',
        'element': '风象星座',
        'ruling_planet': '金星',
        'symbol': '天秤',
        'personality': [
            '优雅和谐',
            '追求公平',
            '善于交际',
            '审美能力强',
            '讲究平衡'
        ],
        'strengths': ['外交能力', '审美能力', '判断力', '协调能力'],
        'weaknesses': ['优柔寡断', '依赖性强', '逃避现实', '表面性格']
    },
    'scorpio': {
        'name': '天蝎座',
        'date_range': '10月24日 - 11月22日',
        'element': '水象星座',
        'ruling_planet': '冥王星',
        'symbol': '天蝎',
        'personality': [
            '神秘深邃',
            '洞察力强',
            '意志坚定',
            '重视感情',
            '追求真理'
        ],
        'strengths': ['洞察力', '意志力', '专注力', '研究能力'],
        'weaknesses': ['多疑', '偏执', '报复心强', '控制欲强']
    },
    'sagittarius': {
        'name': '射手座',
        'date_range': '11月23日 - 12月21日',
        'element': '火象星座',
        'ruling_planet': '木星',
        'symbol': '射手',
        'personality': [
            '乐观开朗',
            '追求自由',
            '爱好冒险',
            '思想开放',
            '诚实直率'
        ],
        'strengths': ['乐观性', '适应能力', '学习能力', '幽默感'],
        'weaknesses': ['轻浮', '缺乏耐心', '言语犀利', '漫不经心']
    },
    'capricorn': {
        'name': '摩羯座',
        'date_range': '12月22日 - 1月19日',
        'element': '土象星座',
        'ruling_planet': '土星',
        'symbol': '摩羯',
        'personality': [
            '务实稳重',
            '目标明确',
            '责任心强',
            '自律性强',
            '追求成功'
        ],
        'strengths': ['组织能力', '耐心', '责任心', '自律性'],
        'weaknesses': ['悲观', '固执', '过分现实', '不够灵活']
    },
    'aquarius': {
        'name': '水瓶座',
        'date_range': '1月20日 - 2月18日',
        'element': '风象星座',
        'ruling_planet': '天王星',
        'symbol': '水瓶',
        'personality': [
            '独特创新',
            '人道主义',
            '理想主义',
            '重视友谊',
            '追求自由'
        ],
        'strengths': ['创新能力', '独立性', '理想主义', '友善'],
        'weaknesses': ['叛逆', '固执己见', '不切实际', '情感淡漠']
    },
    'pisces': {
        'name': '双鱼座',
        'date_range': '2月19日 - 3月20日',
        'element': '水象星座',
        'ruling_planet': '海王星',
        'symbol': '双鱼',
        'personality': [
            '富有同情心',
            '艺术天赋',
            '直觉敏锐',
            '善解人意',
            '富有想象力'
        ],
        'strengths': ['同理心', '艺术能力', '直觉', '适应能力'],
        'weaknesses': ['优柔寡断', '逃避现实', '过分理想化', '意志力弱']
    }
}

# 添加星座配对数据
ZODIAC_COMPATIBILITY = {
    'aries': {
        'aries': {
            'score': 80,
            'love': '两个白羊座的组合充满激情和活力，你们都很有主见，彼此欣赏对方的勇气和领导力。共同的冒险精神让你们的关系充满刺激。',
            'relationship': '建议双方学会适时退让，不要事事争强好胜。在重要决定上要互相商量，给对方表达的机会。',
            'advantages': ['充满激情', '相互理解', '目标一致', '共同进取', '生活刺激'],
            'disadvantages': ['容易争执', '缺乏耐心', '过于直接', '固执己见', '情绪化']
        },
        'taurus': {
            'score': 75,
            'love': '白羊座的活力与金牛座的稳重形成互补，白羊带来激情，金牛带来安全感。这是一个充满张力与平衡的组合。',
            'relationship': '白羊座需要学会耐心，尊重���牛座的节奏；金牛座要试着接受新鲜事物，支持伴侣的冒险精神。',
            'advantages': ['互补性强', '共同成长', '稳定发展', '激情四射', '相互学习'],
            'disadvantages': ['节奏不同', '观念差异', '沟通障碍', '期待不同', '处事方式冲突']
        },
        'gemini': {
            'score': 85,
            'love': '这是一对充满活力的组合！白羊座的热情加上双子座的机智，让你们的关系充满趣味和新鲜感。',
            'relationship': '要注意培养共同兴趣，保持良好沟通。白羊座要理解双子座的多变，双子座要欣赏白羊座的专注。',
            'advantages': ['思维活跃', '充满乐趣', '共同探索', '相互激励', '创意无限'],
            'disadvantages': ['注意力分散', '缺乏稳定', '过于冲动', '难以深入', '情感波动']
        }
        # ... 继续添加其他星座的配对数据
    },
    'taurus': {
        'taurus': {
            'score': 90,
            'love': '两个金牛座的组合非常稳定，你们都重视安全感和物质基础，能够互相理解对方的需求和价值观。',
            'relationship': '要注意避免过于固守，适当尝试新事物。在经济观念上要达成共识，共同规划未来。',
            'advantages': ['价值观一致', '稳定可靠', '相互支持', '生活舒适', '共同目标'],
            'disadvantages': ['过于保守', '缺乏变化', '固执己见', '物质主义', '缺乏激情']
        }
        # ... 继续添加其他星座的配对数据
    }
    # ... 继续添加其他星座的配对数据
}

# 运势评分范围
FORTUNE_RATINGS = ['★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']

# 获取星座基本信息
@app.route('/api/zodiac/<zodiac_sign>', methods=['GET'])
def get_zodiac_info(zodiac_sign):
    zodiac_info = ZODIAC_DATA.get(zodiac_sign.lower())
    if not zodiac_info:
        return jsonify({'error': '未找到该星座信息'}), 404
    return jsonify(zodiac_info)

# 获取运势信息
@app.route('/api/horoscope/<zodiac_sign>/<period>', methods=['GET'])
def get_horoscope(zodiac_sign, period):
    if zodiac_sign.lower() not in ZODIAC_DATA:
        return jsonify({'error': '未找到该星座信息'}), 404
        
    if period not in ['daily', 'weekly', 'monthly', 'yearly']:
        return jsonify({'error': '无效的时间周期'}), 400

    # 获取星座基本信息
    zodiac_info = ZODIAC_DATA[zodiac_sign.lower()]
    
    # 根据星座特点生成运势描述
    def generate_description():
        personality = zodiac_info['personality']
        strengths = zodiac_info['strengths']
        element = zodiac_info['element']
        
        descriptions = {
            'daily': {
                'overall': f'今天的{zodiac_info["name"]}整体运势不错，{personality[0]}的特质会带来好运。充分发挥{strengths[0]}，会有意外收获。',
                'love': f'感情方面，{element}的特质让你魅力四射。单身的{zodiac_info["name"]}可能遇到心动的对象，已有伴侣的会享受甜蜜时光。',
                'career': f'工作上，你的{strengths[1]}得到充分发挥。同事和领导都会欣赏你的表现，可能有加薪或升职的机会。',
                'wealth': f'财运方面，建议发挥{zodiac_info["name"]}的{personality[1]}特质。适合投资理财，但要注意控制风险。',
                'health': f'健康方面要注意调节。{zodiac_info["name"]}的{personality[2]}特质可能导致过度劳累，记得适当休息。'
            },
            'weekly': {
                'overall': f'本周{zodiac_info["name"]}运势平稳，特别是在{strengths[0]}方面会有突出表现。',
                'love': f'感情运势温和，{personality[3]}的特质会助你擦出爱情火花。已有伴侣的要多关心对方。',
                'career': f'事业发展顺利，{strengths[2]}让你在工作中脱颖而出。可能收到重要项目或升职机会。',
                'wealth': f'理财方面要发挥{zodiac_info["name"]}的{personality[1]}特质，合理规划支出，可能有意外收入。',
                'health': f'保持{personality[4]}的生活态度，注意作息规律，适当运动放松。'
            },
            'monthly': {
                'overall': f'本月{zodiac_info["name"]}运势起伏，以{strengths[0]}和{strengths[1]}应对挑战。',
                'love': f'感情生活精彩，{element}的特质让你在感情中占据主动。单身者可能遇到理想对象。',
                'career': f'工作上有新的机遇，充分发挥{strengths[2]}和{strengths[3]}，会有不错的发展。',
                'wealth': f'财运较，适合规划长期投资。{zodiac_info["name"]}的{personality[1]}特质会带来财运。',
                'health': f'健康状况稳定，保持{personality[4]}的生活态度，注意劳逸结合。'
            },
            'yearly': {
                'overall': f'{zodiac_info["name"]}今年运势不错，{element}的能量带来好运。重点发展{strengths[0]}方面。',
                'love': f'感情运势旺盛，{personality[3]}的特质让你在感情中收获满满。可能有重要的感情突破。',
                'career': f'事业发展机会多，{strengths[1]}和{strengths[2]}会帮助你实现职业目标。',
                'wealth': f'财运整体向好，{zodiac_info["name"]}的{personality[1]}特质会带来不错的收益。',
                'health': f'身心健康是关键，保持{personality[4]}的生活态度，规律作息很重要。'
            }
        }
        return descriptions[period]

    # 生成运势数据
    fortune = {
        'overall': random.choice(FORTUNE_RATINGS),
        'love': random.choice(FORTUNE_RATINGS),
        'career': random.choice(FORTUNE_RATINGS),
        'wealth': random.choice(FORTUNE_RATINGS),
        'health': random.choice(FORTUNE_RATINGS),
        'description': generate_description()
    }

    # 添加时间信息
    current_date = datetime.now()
    if period == 'daily':
        date_info = current_date.strftime('%Y年%m月%d日')
    elif period == 'weekly':
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        date_info = f"{week_start.strftime('%Y年%m月%d日')} 至 {week_end.strftime('%Y年%m月%d日')}"
    elif period == 'monthly':
        date_info = current_date.strftime('%Y年%m月')
    else:  # yearly
        date_info = current_date.strftime('%Y年')

    fortune['period'] = {
        'type': period,
        'date': date_info
    }

    return jsonify(fortune)

# 添加配对分析API
@app.route('/api/compatibility/<zodiac1>/<zodiac2>', methods=['GET'])
def get_compatibility(zodiac1, zodiac2):
    zodiac1 = zodiac1.lower()
    zodiac2 = zodiac2.lower()
    
    if zodiac1 not in ZODIAC_DATA or zodiac2 not in ZODIAC_DATA:
        return jsonify({'error': '无效的星座'}), 400
        
    # 获取两个星座的基本信息
    zodiac1_info = ZODIAC_DATA[zodiac1]
    zodiac2_info = ZODIAC_DATA[zodiac2]
    
    # 获取配对数据，如果没有特定配对数据，使用默认生成的数据
    compatibility = ZODIAC_COMPATIBILITY.get(zodiac1, {}).get(zodiac2)
    if not compatibility:
        # 如果没有直接的配对数据，尝试反向查找
        compatibility = ZODIAC_COMPATIBILITY.get(zodiac2, {}).get(zodiac1)
    
    if not compatibility:
        # 如果没有预定义的配对数据，生成默认数据
        compatibility = generate_default_compatibility(zodiac1_info, zodiac2_info)
    
    # 构建详细的配对分析
    result = {
        'score': compatibility['score'],
        'analysis': {
            'overall': compatibility['love'],
            'relationship': compatibility['relationship'],
            'advantages': compatibility['advantages'],
            'disadvantages': compatibility['disadvantages']
        },
        'zodiac1': {
            'name': zodiac1_info['name'],
            'element': zodiac1_info['element'],
            'personality': zodiac1_info['personality'][:3]
        },
        'zodiac2': {
            'name': zodiac2_info['name'],
            'element': zodiac2_info['element'],
            'personality': zodiac2_info['personality'][:3]
        }
    }
    
    return jsonify(result)

def generate_default_compatibility(zodiac1, zodiac2):
    """生成默认的配对分析数据"""
    # 根据星座元素计算基础分数
    base_score = calculate_element_compatibility(zodiac1['element'], zodiac2['element'])
    
    return {
        'score': base_score,
        'love': f"{zodiac1['name']}和{zodiac2['name']}的组合很有趣。{zodiac1['name']}的{zodiac1['personality'][0]}特质与{zodiac2['name']}的{zodiac2['personality'][0]}特质形成独特的互动。你们的组合充满了发展潜力。",
        'relationship': f"建议{zodiac1['name']}发挥{zodiac1['strengths'][0]}的优势，而{zodiac2['name']}则可以用{zodiac2['strengths'][0]}来平衡。互相理解对方的特点，会让关系更加和谐。",
        'advantages': [
            f"共同的{zodiac1['strengths'][0]}精神",
            f"{zodiac1['name']}的{zodiac1['personality'][1]}与{zodiac2['name']}的{zodiac2['personality'][1]}相得益彰",
            f"能够在{zodiac1['strengths'][1]}方面互相支持",
            f"在{zodiac2['strengths'][1]}领域有共同话题",
            "有助于共同成长"
        ],
        'disadvantages': [
            f"{zodiac1['name']}的{zodiac1['weaknesses'][0]}可能与{zodiac2['name']}产生分歧",
            f"{zodiac2['name']}的{zodiac2['weaknesses'][0]}需要多加注意",
            "需要更多的沟通和理解",
            "可能在决策方式上存在分歧",
            "处事方式需要相互适应"
        ]
    }

def calculate_element_compatibility(element1, element2):
    """计算星座元素相性分数"""
    element_scores = {
        ('火象星座', '火象星座'): 85,
        ('火象星座', '风象星座'): 90,
        ('火象星座', '土象星座'): 75,
        ('火象星座', '水象星座'): 65,
        ('土象星座', '土象星座'): 95,
        ('土象星座', '水象星座'): 90,
        ('土象星座', '风象星座'): 70,
        ('水象星座', '水象星座'): 95,
        ('水象星座', '风象星座'): 75,
        ('风象星座', '风象星座'): 85,
    }
    
    pair = tuple(sorted([element1, element2]))
    return element_scores.get(pair, 75)  # 默认返回75分

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000) 