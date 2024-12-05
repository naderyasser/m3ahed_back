# Improved Flask app

from flask import Flask, render_template, request, redirect, url_for, flash, session ,send_from_directory ,blueprints , Blueprint, jsonify , request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from flask_migrate import Migrate
from datetime import datetime
import os
import uuid
from flask import request, jsonify
from sqlalchemy import or_
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')



app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')
# max upload size 100MB
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this key
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(255), nullable=True)
    views = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='draft')  # draft, published
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    media = db.relationship('Media', backref='post', lazy=True)

    def to_dict(self, base_url):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'content': self.content,
            'banner_url': f"{base_url}/uploads/{self.banner}" if self.banner else None,
            'views': self.views,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'media': [media.to_dict(base_url) for media in self.media],
        }

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # image, video, audio, document 
    url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, published
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, base_url):
        return {
            'id': self.id,
            'name': self.name,
            'media_type': self.media_type,
            'url': f"{base_url}/uploads/{self.url}",
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }


class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(255), unique=True, nullable=False)
      password = db.Column(db.String(255), nullable=False)
      email = db.Column(db.String(255), unique=True, nullable=False)
      status = db.Column(db.String(50), default='active')  # active, inactive
      created_at = db.Column(db.DateTime, default=datetime.utcnow)
      updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# blueprint for admin routes

admin = Blueprint('admin', __name__, url_prefix='/admin')
api = Blueprint('api', __name__, url_prefix='/api')
def save_file(file):
    filename = file.filename
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        file_ext = filename.rsplit('.', 1)[1].lower()
        filename = str(uuid.uuid4()) + '.' + file_ext
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None


@app.route('/')
def index():
      last_3_news = Post.query.filter_by(category='news').order_by(Post.created_at.desc()).limit(3).all()
      return render_template('public/index.html', news=last_3_news)

@app.route('/posts/<category>')
def posts(category):
      posts = Post.query.filter_by(category=category).all()
      if not posts:
            flash('No posts found', 'danger')
            return redirect(url_for('index'))
      return render_template('public/list.html', PageName=category, posts=posts)
@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    post.views += 1  
    db.session.commit()
    media = Media.query.filter_by(post_id=id).all()  # Retrieve all media associated with the post
    return render_template('public/post.html', post=post, media=media)


# respoens with data from the uploads folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
      return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@admin.route('/')
def index():
    # Example static data for the cards
    stats = {
        'media_count': Media.query.count(),
        'post_views': sum(post.views for post in Post.query.all()),
        'storage_used': '15GB',  # Assuming you calculate this somehow
        'visitors_count': 1200  # Example count
    }
    # Fetch data for the table (last 10 posts)
    latest_table_posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()

    return render_template('admin/index.html', stats=stats, latest_table_posts=latest_table_posts)

@admin.route('/list/<category>')
def list(category):
      posts = Post.query.filter_by(category=category).all()
      return render_template('admin/list.html', latest_table_posts=posts,category=category)


# add_post
@admin.route('/add', methods=['GET', 'POST'])
def add_post():
      if request.method == 'POST':
            title = request.form['title']
            category = request.form['category']
            content = request.form['content']
            banner = request.files['image']
            status = request.form['status']

            post = Post(title=title, category=category, content=content, banner=save_file(banner), status=status)
            db.session.add(post)
            db.session.commit()
            flash('Post added successfully', 'success')
            return redirect(url_for('admin.index'))
      return render_template('admin/add.html')

@admin.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    media_items = Media.query.filter_by(post_id=id).all()

    if request.method == 'POST':
        print(request.files)
        file = request.files.get('file')
        media_type = request.form.get('media_type')
        if file and media_type :
            filename = save_file(file)
            if filename:
                new_media = Media(name=filename, post_id=id, media_type=media_type, url=os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.session.add(new_media)
                db.session.commit()
                flash('Media added successfully', 'success')
            else:
                flash('Failed to save file', 'danger')
        else:
            flash('Invalid file type', 'warning')

    return render_template('admin/post.html', post=post, media_items=media_items)

# admin.edit_post
@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
      post = Post.query.get(id)
      if request.method == 'POST':
            post.title = request.form['title']
            post.category = request.form['category']
            post.content = request.form['content']

            post.status = request.form['status']
            db.session.commit()
            flash('Post updated successfully', 'success')
            return redirect(url_for('admin.post', id=post.id))
      return render_template('admin/edit.html', post=post)
# admin.delete_post
@admin.route('/delete/<int:id>')
def delete_post(id):
      post = Post.query.get(id)
      db.session.delete(post)
      db.session.commit()
      flash('Post deleted successfully', 'success')
      return redirect(url_for('admin.index'))

# admin.delete_media
@admin.route('/media/delete/<int:id>')
def delete_media(id):
    media = Media.query.get(id)
    db.session.delete(media)
    db.session.commit()
    flash('Media deleted successfully', 'success')
    return redirect(url_for('admin.post', id=media.post_id))

@api.route('/posts', methods=['GET'])
def get_posts():
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    page = int(request.args.get('page', 1))  
    limit = int(request.args.get('limit', 10))  
    sort_by = request.args.get('sort_by', 'created_at')  
    order = request.args.get('order', 'desc') 

    query = Post.query

    if category:
        query = query.filter(Post.category == category)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Post.title.ilike(search_term),
                Post.content.ilike(search_term)
            )
        )

    if order == 'asc':
        query = query.order_by(getattr(Post, sort_by).asc())
    else:
        query = query.order_by(getattr(Post, sort_by).desc())

    total_items = query.count()
    posts = query.paginate(page=page, per_page=limit, error_out=False).items

    base_url = request.url_root.rstrip('/')

    response = {
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items + limit - 1) // limit, 
        "posts": [post.to_dict(base_url) for post in posts]
    }
    return jsonify(response), 200

@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post=post.to_dict(request.host_url)), 200

@api.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Use hashed password in production
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@api.route('/posts', methods=['POST'])
@jwt_required()
def add_post_api():
    title = request.json.get('title')
    category = request.json.get('category')
    content = request.json.get('content')
    status = request.json.get('status')
    banner = request.files.get('banner')

    if not title or not category or not content:
        return jsonify(message="Missing required fields"), 400

    filename = save_file(banner) if banner else None
    post = Post(title=title, category=category, content=content, banner=filename, status=status)
    db.session.add(post)
    db.session.commit()
    return jsonify(post=post.to_dict(request.host_url)), 201

@api.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def edit_post_api(id):
    post = Post.query.get_or_404(id)
    
    post.title = request.json.get('title', post.title)
    post.category = request.json.get('category', post.category)
    post.content = request.json.get('content', post.content)
    post.status = request.json.get('status', post.status)
    
    db.session.commit()
    return jsonify(post=post.to_dict(request.host_url)), 200

@api.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post_api(id):
    post = Post.query.get_or_404(id)
    
    # Delete associated media
    for media_item in post.media:
        db.session.delete(media_item)
    
    db.session.delete(post)
    db.session.commit()
    return jsonify(message="Post deleted successfully"), 200
@api.route('/posts/<int:id>/media', methods=['POST'])
@jwt_required()
def add_media_to_post_api(id):
    post = Post.query.get_or_404(id)
    file = request.files.get('file')
    media_type = request.json.get('media_type')

    if not file or not media_type:
        return jsonify(message="Missing required fields"), 400

    filename = save_file(file)
    if filename:
        media = Media(name=filename, post_id=id, media_type=media_type, url=os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(media)
        db.session.commit()
        return jsonify(media=media.to_dict(request.host_url)), 201
    return jsonify(message="File save failed"), 500

@api.route('/media/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_media_api(id):
    media = Media.query.get_or_404(id)
    db.session.delete(media)
    db.session.commit()
    return jsonify(message="Media deleted successfully"), 200

# register the blueprint
app.register_blueprint(admin)
app.register_blueprint(api)




if __name__ == '__main__':
      with app.app_context():
            db.create_all()
      app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)

