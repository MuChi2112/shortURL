from flask import Flask, request, render_template_string, redirect
import base64  # 使用 base64 作示範，base62 需要額外安裝或自訂

app = Flask(__name__)

# 模擬資料庫
urls = {}

# 使用 base64 替代 base62 進行簡單編碼（你可以用真正的 base62）
def shorten_url(url):
    encoded = base64.urlsafe_b64encode(url.encode()).decode()
    return encoded[:8]  # 簡化

# 首頁
@app.route('/')
def home():
    return 'Hello, Flask!'

# 表單頁面
@app.route('/form')
def form():
    return render_template_string('''
        <h2>縮網址服務</h2>
        <form action="/add_url" method="post">
            原始網址：<input name="url">
            <input type="submit" value="縮短">
        </form>
        <br>
        <form action="/get_url" method="get">
            短碼：<input name="code">
            <input type="submit" value="查詢原始網址">
        </form>
    ''')

# 新增縮網址（POST）
@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.form['url']
    short = shorten_url(url)
    urls[short] = url
    return f'新增成功！短網址代碼是：<b>{short}</b>'

# 查詢原網址（GET）

@app.route('/<short_code>')
def redirect_to_external(short_code):
    if short_code in urls:
        org_url = urls[short_code]
        return redirect(org_url)
    else:
        return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
