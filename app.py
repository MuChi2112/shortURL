from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, Flask!'

# 模擬資料庫（列表）
users = ['Alice', 'Bob']

# Read 所有使用者
@app.route('/users')
def list_users():
    return '<br>'.join(f'{i}: {name}' for i, name in enumerate(users))

# Create 新使用者： /add/Charlie
@app.route('/add/<name>')
def add_user(name):
    users.append(name)
    return f'Added {name}'

# Read 單一使用者： /user/1
@app.route('/user/<int:user_id>')
def get_user(user_id):
    if user_id < 0 or user_id >= len(users):
        return 'User not found', 404
    return f'User {user_id}: {users[user_id]}'

# Update 使用者名字： /update/1/John
@app.route('/update/<int:user_id>/<new_name>')
def update_user(user_id, new_name):
    if user_id < 0 or user_id >= len(users):
        return 'User not found', 404
    old_name = users[user_id]
    users[user_id] = new_name
    return f'Updated {old_name} to {new_name}'

# Delete 使用者： /delete/1
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    if user_id < 0 or user_id >= len(users):
        return 'User not found', 404
    name = users.pop(user_id)
    return f'Deleted {name}'

if __name__ == '__main__':
    app.run(debug=True)