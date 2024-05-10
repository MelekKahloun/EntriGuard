from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
content = [
    {
        'title': 'Pembuatan Aplikasi Android',
    }
]

@app.route('/')
def index():
    return render_template('index.html', 
                           posts=content,
                           title='Cute Blog 🥳', 
                           description='A modern web blog template for flask with auto SEO from cuteblog',
                           cover='https://www.python.org/static/opengraph-icon-200x200.png'
                          )
	
@app.route('/cutelist')
def cutelist():
    return render_template('cutelist.html', 
                           posts=content,
                           title='Cute List Blog 🥳', 
                           description='A modern web blog template for flask with auto SEO from cuteblog',
                           cover='https://www.python.org/static/opengraph-icon-200x200.png'
                          )

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((item for item in content if item['id'] == post_id), None)
    return render_template('post.html', 
                           post=post
                          )
	
@app.route('/delete/<int:post_id>')
def delete(post_id):
    global content
    content = [item for item in content if item['id'] != post_id]
    return redirect('/cutelist')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    global content
    post = next((item for item in content if item['id'] == post_id), None)

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['subtitle'] = request.form['subtitle']
        post['author'] = request.form['author']
        post['content'] = request.form['content']
        post['cover'] = request.form['cover']

        return redirect('/cutelist')

    else:
        return render_template('update.html', post=post)

@app.route('/cute')
def add():
    return render_template('cute.html')

@app.route('/cutepost', methods=['POST'])
def cutepost():
    global content
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    cover = request.form['cover']
    
    new_post = {
        'id': len(content) + 1, # Generating unique id
        'title': title,
        'subtitle': subtitle,
        'author': author,
        'content': content,
        'cover': cover,
        'date_posted': datetime.now()
    }
    content.append(new_post)

    return redirect(url_for('cutelist'))

if __name__ == '__main__':
    app.run(debug=True)
