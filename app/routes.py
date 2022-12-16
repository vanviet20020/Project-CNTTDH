import json
import os
from app import app
from app.models import *
from app.form import *
from sqlalchemy import or_
from sqlalchemy import func
from flask import request, render_template, redirect, flash, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.upload import allowed_file


@app.route('/')
def index():
    movies=Movie.query.all()
    return render_template('index.html', movies=movies, title='Rạp chiếu phim')

@app.route("/movies/detail/<int:id_movie>")
def detail_movie(id_movie):
    movie = Movie.query.get(id_movie)
    return render_template("Movies/detail.html", movie=movie, title="Thông tin phim " + movie.name)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # tạo biến form từ class SignUpForm bên form.py
    form = SignUpUser()
    if form.validate_on_submit() and request.method == 'POST':
        new_user = User(
            fullname=form.fullname.data,
            email=form.email.data,
            password=form.password.data,
            phone_number=form.phone_number.data,
            gender=form.gender.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Tạo tài khoản thành công! Đăng nhập ngay')
        return redirect(url_for('login'))
    return render_template('Users/sign_up.html', form=form, title='Đăng kí tài khoản')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Tài khoản hoặc mật khẩu chưa chính xác!')
            return redirect(url_for('login'))

        # Hàm lưu tên tài khoản khi đăng nhập thành công
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('Users/login.html', title='Đăng nhập', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Đăng xuất thành công!')
    return redirect(url_for('index'))


@app.route('/management/users')
@login_required
def management_users():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        users = User.query.all()
        return render_template(
            'Users/management_page.html', users=users, title='Quản lý tài khoản'
        )


# Tìm users theo fullname hoặc email
@app.route('/management/users/search')
@login_required
def management_search_users():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        data_search = request.args.get('data_search')
        if data_search and len(data_search) >= 1:
            users = User.query.filter(
                or_(
                    User.fullname.ilike(f'%{data_search}%'),
                    User.email.ilike(f'%{data_search}%'),
                    User.phone_number.ilike(f'%{data_search}%')
                )
            ).all()
            if users and len(users) >= 1:
                return render_template(
                    'Users/management_page.html', users=users, title='Quản lý tài khoản'
                )
            else:
                flash('Không tìm thấy giá trị nhập')
                return redirect(url_for('management_users'))
        else:
            flash('Giá trị nhập không đúng xin nhập lại!')
            return redirect(url_for('management_users'))


@app.route('/management/users/update/<int:id_user>', methods=['GET', 'POST'])
@login_required
def update_user(id_user):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        user = User.query.get(id_user)
        form = UpdateUser()
        if form.validate_on_submit() and request.method == 'POST':
            user.fullname = form.fullname.data
            user.phone_number = form.phone_number.data
            user.gender = form.gender.data
            if form.is_admin.data == 'Không':
                new_is_admin = False
            else:
                new_is_admin = True
            user.is_admin = new_is_admin
            db.session.commit()
            flash('Cập nhật thông tin tài khoản thành công !')
            return redirect(url_for('management_users'))
        return render_template(
            'Users/update.html',
            user=user,
            form=form,
            title='Cập nhật thông tin tài khoản',
        )


@app.route('/management/users/delete/<int:id_user>')
def delete_user(id_user):
    user = User.query.get(id_user)
    db.session.delete(user)
    db.session.commit()
    flash('Xóa tài khoản thành công')
    return redirect(url_for('management_users'))


@app.route('/management/suppliers/create', methods=['GET', 'POST'])
@login_required
def create_supplier():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        form = SupplierForm()
        if form.validate_on_submit() and request.method == 'POST':
            name = form.name.data
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)
            photo = request.files['photo']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if photo.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), 'static/img/Suppliers/', filename))
                new_supplier = Supplier(name=name, img_price_ticket=filename)
                db.session.add(new_supplier)
                db.session.commit()
                return redirect(url_for('management_suppliers'))
    return render_template('Suppliers/create.html', form=form, title='Thêm nhà cung cấp')


@app.route('/management/suppliers')
@login_required
def management_suppliers():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        suppliers = Supplier.query.all()
        return render_template('suppliers/management_page.html', suppliers=suppliers, title='Quản lý nhà cung cấp')


@app.route('/management/suppliers/search')
@login_required
def management_search_supplier():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        data_search = request.args.get('data_search')
        if data_search and len(data_search) >= 1:
            supplier = Supplier.query.filter(
                Supplier.name.ilike(f'%{data_search}%')).all()
            if supplier and len(supplier) >= 1:
                return render_template(
                    'Suppliers/management_page.html', supplier=supplier, title='Quản lý tài khoản'
                )
            else:
                flash('Không tìm thấy giá trị nhập')
                return redirect(url_for('management_suppliers'))
        else:
            flash('Giá trị nhập không đúng xin nhập lại!')
            return redirect(url_for('management_suppliers'))


@app.route('/management/suppliers/update/<int:id_supplier>', methods=['GET', 'POST'])
@login_required
def update_supplier(id_supplier):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        form = SupplierForm()
        if form.validate_on_submit() and request.method == 'POST':
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)
            photo = request.files['photo']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if photo.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), 'static/img/Suppliers/', filename))

                supplier = Supplier.query.get(id_supplier)
                supplier.name = form.name.data
                supplier.img_price_ticket = filename
                db.session.commit()
                flash('Cập nhật thông tin nhà cung cấp thành công !')
                return redirect(url_for('management_suppliers'))
        return render_template('Suppliers/update.html', form=form, title='Cập nhật thông tin nhà cung cấp')


@app.route('/management/suppliers/delete/<int:id_supplier>')
def delete_supplier(id_supplier):
    supplier = Supplier.query.get(id_supplier)
    db.session.delete(supplier)
    db.session.commit()
    flash('Xóa nhà cung cấp khoản thành công')
    return redirect(url_for('management_suppliers'))


@app.route('/management/cinemas/create', methods=['GET', 'POST'])
@login_required
def create_cinema():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        suppliers = Supplier.query.all()
        form = CinemaForm()
        if form.validate_on_submit() and request.method == 'POST':
            id_supplier = int(request.form.get('id_supplier'))
            # lấy giá trị lat long và gán vào biến geoCinema dưới dạng điểm
            geomCinema = "Point(" + form.lng.data + " " + form.lat.data + ")"
            new_cinema = Cinema(
                id_supplier=id_supplier,
                name=form.name.data,
                district=form.district.data,
                address=form.address.data,
                hotline=form.hotline.data,
                geom=func.ST_GeomFromText(geomCinema, 4326)
            )
            db.session.add(new_cinema)
            db.session.commit()
            flash('Thêm rạp chiếu phim mới thành công!')
            return redirect(url_for('management_cinemas'))
        return render_template(
            'Cinemas/create.html', suppliers=suppliers, form=form, title='Thêm rạp chiếu phim mới'
        )


@app.route('/cinemas')
def get_all_cinemas():
    cinemas = Cinema.query.all()
    return render_template(
        'Cinemas/index.html',
        cinemas=cinemas,
        title='Tất cả các rạp chiếu phim',
    )


@app.route('/cinemas/search')
def search_cinemas():
    data_search = request.args.get('data_search')
    if data_search and len(data_search) >= 1:
        cinemas = Cinema.query.filter(
            or_(
                Cinema.name.ilike(f'%{data_search}%'),
                Cinema.address.ilike(f'%{data_search}%'),
            )
        ).all()
        if cinemas and len(cinemas) >= 1:
            return render_template(
                'Cinemas/index.html',
                cinemas=cinemas,
                title='Tất cả các rạp chiếu phim',
            )
        else:
            flash('Không tìm thấy giá trị nhập')
            return redirect(url_for('get_all_cinemas'))
    else:
        flash('Giá trị nhập không đúng xin nhập lại!')
        return redirect(url_for('get_all_cinemas'))


# API trả về dữ liệu json của Cinema
@app.route('/api/cinemas')
def api_get_all_cinemas():
    cinemas = db.session.query(
        Cinema.id,
        Cinema.name,
        Cinema.district,
        Cinema.address,
        Cinema.hotline,
        func.ST_AsGeoJSON(Cinema.geom).label('geometry'),
    ).all()
    cinemasFeatures = []
    for cinema in cinemas:
        properties_temp = {
            'id': cinema.id,
            'name': cinema.name,
            'district': cinema.district,
            'address': cinema.address,
            'hotline': cinema.hotline,
        }
        geometry_temp = json.loads(cinema.geometry)
        cinema_temp = {
            'type': 'Feature',
            'properties': properties_temp,
            'geometry': geometry_temp,
        }
        cinemasFeatures.append(cinema_temp)
    return jsonify({'features': cinemasFeatures})


@app.route('/cinemas/maps')
def view_cinema_maps():
    return render_template('Cinemas/view_cinema_maps.html', title='Xem vị trí rạp')


@app.route('/management/cinemas')
@login_required
def management_cinemas():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        cinemas = Cinema.query.all()
        return render_template(
            'Cinemas/management_page.html',
            cinemas=cinemas,
            title='Quản lý rạp chiếu phim',
        )


@app.route('/management/cinemas/search')
@login_required
def management_cinemas_search():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        data_search = request.args.get('data_search')
        if data_search and len(data_search) >= 1:
            cinemas = Cinema.query.filter(
                or_(
                    Cinema.name.ilike(f'%{data_search}%'),
                    Cinema.address.ilike(f'%{data_search}%'),
                )
            ).all()
            if cinemas and len(cinemas) >= 1:
                return render_template(
                    'Cinemas/management_page.html',
                    cinemas=cinemas,
                )
            else:
                flash('Không tìm thấy giá trị nhập')
                return redirect(url_for('management_cinemas'))
        else:
            flash('Giá trị nhập không đúng xin nhập lại!')
            return redirect(url_for('management_cinemas'))


@app.route('/management/cinemas/update/<int:id_cinema>', methods=['GET', 'POST'])
@login_required
def update_cinema(id_cinema):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        suppliers = Supplier.query.all()
        form = CinemaForm()
        if form.validate_on_submit() and request.method == 'POST':
            id_supplier = int(request.form.get('id_supplier'))
            cinema = Cinema.query.get(id_cinema)
            cinema.id_supplier = id_supplier
            cinema.name = form.name.data
            cinema.address = form.address.data
            cinema.district = form.district.data
            cinema.hotline = form.hotline.data
            geomCinema = "Point(" + form.lng.data + " " + form.lat.data + ")"
            new_geom = func.ST_GeomFromText(geomCinema, 4326)
            cinema.geom = new_geom
            db.session.commit()
            flash('Cập nhật thông tin rạp thành công!')
            return redirect(url_for('get_all_cinemas'))

        return render_template(
            'Cinemas/update.html',
            suppliers=suppliers,
            id_cinema=id_cinema,
            form=form,
            title='Cập nhật thông tin rạp chiếu phim',
        )


@app.route('/management/cinemas/delete/<int:id_cinema>')
@login_required
def delete_cinema(id_cinema):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        cinema = Cinema.query.get(id_cinema)
        db.session.delete(cinema)
        db.session.commit()
        flash('Xóa vị trí rạp ' + cinema.name + 'thành công!')
        return redirect(url_for('management_cinemas'))


@app.route('/cinemas/<int:id_cinema>', methods=['GET', 'POST'])
def detail_cinema(id_cinema):
    cinema = Cinema.query.get(id_cinema)
    form = EvaluateForm()
    if form.validate_on_submit() and request.method == 'POST':
        id_user = current_user.id
        evaluate = Evaluate(
            id_user=id_user, id_cinema=id_cinema,
            content=form.content.data, start_rated=form.star_rated.data)
        db.session.add(evaluate)
        db.session.commit()
        flash('Thêm đánh giá thành công')
    return render_template('Cinemas/detail.html', form=form, cinema=cinema, title=cinema.name)


@app.route('/management/movies/create', methods=['GET', 'POST'])
@login_required
def create_movie():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        form = MovieForm()
        if form.validate_on_submit() and request.method == 'POST':
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)
            photo = request.files['photo']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if photo.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), 'static/img/Movies/', filename))
                new_movie = Movie(
                    name=form.name.data, img=filename,
                    describe=form.describe.data, director=form.director.data,
                    actor=form.actor.data, genre=form.genre.data, release_date=form.release_date.data,
                    running_time=form.running_time.data, language=form.language.data, rated=form.rated.data
                )
                db.session.add(new_movie)
                db.session.commit()
                flash('Thêm mới phim thành công!')
                return redirect(url_for('management_movies'))
        return render_template('Movies/create.html', form=form, title='Thêm phim mới')


@app.route('/movies')
def get_all_movies():
    movies = Cinema.query.all()
    return render_template('Movies/index.html', movies=movies, title='Danh sách phim đang chiếu')


@app.route('/movies/search')
def search_movies():
    data_search = request.args.get('data_search')
    if data_search and len(data_search) >= 1:
        movies = Movie.query.filter(
            or_(
                Movie.name.ilike(f'%{data_search}%'),
                Movie.director.ilike(f'%{data_search}%'),
                Movie.actor.ilike(f'%{data_search}%'),
                Movie.genre.ilike(f'%{data_search}%')
            )
        ).all()
        if movies and len(movies) >= 1:
            return render_template(
                'Movies/index.html',
                movies=movies,
                title='Danh sách phim đang chiếu'
            )
        else:
            flash('Không tìm thấy giá trị nhập')
            return redirect(url_for('get_all_cinemas'))
    else:
        flash('Giá trị nhập không đúng xin nhập lại!')
        return redirect(url_for('get_all_cinemas'))


@app.route('/management/movies')
def management_movies():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        movies = Movie.query.all()
        return render_template('Movies/management_page.html', movies=movies, title='Quản lý phim đang chiếu')


@app.route('/management/movies/search')
def management_search_movies():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        data_search = request.args.get('data_search')
        if data_search and len(data_search) >= 1:
            movies = Movie.query.filter(
                or_(
                    Movie.name.ilike(f'%{data_search}%'),
                    Movie.director.ilike(f'%{data_search}%'),
                    Movie.actor.ilike(f'%{data_search}%'),
                    Movie.genre.ilike(f'%{data_search}%')
                )
            ).all()
            if movies and len(movies) >= 1:
                return render_template(
                    'Movies/management_page.html',
                    movies=movies,
                    title='Quản lý phim đang chiếu'
                )
            else:
                flash('Không tìm thấy giá trị nhập')
                return redirect(url_for('management_movies'))
        else:
            flash('Giá trị nhập không đúng xin nhập lại!')
            return redirect(url_for('management_movies'))


@app.route('/management/movies/update/<int:id_movie>', methods=['GET', 'POST'])
@login_required
def update_movie(id_movie):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        form = MovieForm()
        if form.validate_on_submit() and request.method == 'POST':
            if 'photo' not in request.files:
                flash('No file part')
                return redirect(request.url)
            photo = request.files['photo']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if photo.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(os.path.abspath(os.path.dirname(
                    __file__)), 'static/img/Movies/', filename))
                movie = Movie.query.get(id_movie)
                movie.name = form.name.data
                movie.img = filename
                movie.describe = form.describe.data
                movie.director = form.director.data
                movie.actor = form.actor.data
                movie.genre = form.genre.data
                movie.release_date = form.release_date.data
                movie.rated = form.rated.data
                movie.language = form.language.data
                db.session.commit()
                flash('Cập nhật thông tin phim thành công!')
                return redirect(url_for('management_movies'))
        return render_template(
            'Movies/update.html',
            id_movie=id_movie,
            form=form,
            title='Cập nhật thông tin rạp chiếu phim',
        )


@app.route('/management/movies/delete/<int:id_movie>')
@login_required
def delete_movie(id_movie):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        movie = Movie.query.get(id_movie)
        db.session.delete(movie)
        db.session.commit()
        flash('Xóa vị trí rạp ' + movie.name + ' thành công!')
        return redirect(url_for('management_movies'))


@app.route('/management/movie_showtimes/create', methods=['GET', 'POST'])
@login_required
def create_movie_showtime():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        cinemas = Cinema.query.all()
        movies = Movie.query.all()
        form = MovieShowtimeForm()
        if form.validate_on_submit() and request.method == 'POST':
            id_cinema = int(request.form.get("id_cinema"))
            id_movie = int(request.form.get("id_movie"))
            new_movie_showtime = Movie_showtime(
                id_cinema=id_cinema,
                id_movie=id_movie,
                screening_date=form.screening_date.data,
                time_start=form.time_start.data,
                seats=form.seats.data
            )
            db.session.add(new_movie_showtime)
            db.session.commit()
            flash("Thêm lịch chiếu phim thành công!")
            return redirect(url_for('management_movie_showtimes'))
        return render_template('Movie_Showtimes/create.html', form=form, cinemas=cinemas, movies=movies, title="Tạo lịch chiếu phim")


@app.route('/management/movie_showtime')
@login_required
def management_movie_showtimes():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        movie_showtimes = Movie_showtime.query.all()
        return render_template('Movie_Showtimes/management_page.html', movie_showtimes=movie_showtimes, title="Quản lý lích chiếu phim")


@app.route('/management/movie_showtimes/search')
def management_search_movie_showtimes():
    data_search = request.args.get('data_search')
    if data_search and len(data_search) >= 1:
        movie_showtimes = Movie_showtime.query.filter(
            or_(
                Movie_showtime.screening_date.ilike(f'%{data_search}%'),
                Movie_showtime.time_start.ilike(f'%{data_search}%'),
            )
        ).all()
        if movie_showtimes and len(movie_showtimes) >= 1:
            return render_template(
                'Movie_showtimes/management_page.html',
                movie_showtimes=movie_showtimes,
                title='Quản lý lịch chiếu phim'
            )
        else:
            flash('Không tìm thấy giá trị nhập')
            return redirect(url_for('management_movie_showtimes'))
    else:
        flash('Giá trị nhập không đúng xin nhập lại!')
        return redirect(url_for('management_movie_showtimes'))


@app.route('/management/movie_showtimes/update/<int:id_movie_showtime>',  methods=['GET', 'POST'])
@login_required
def update_movie_showtime(id_movie_showtime):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        cinemas = Cinema.query.all()
        movies = Movie.query.all()
        form = MovieShowtimeForm()
        if form.validate_on_submit() and request.method == 'POST':
            id_cinema = int(request.form.get("id_cinema"))
            id_movie = int(request.form.get("id_movie"))
            movie_showtime = Movie_showtime.query.get(id_movie_showtime)
            movie_showtime.id_cinema = id_cinema
            movie_showtime.id_movie = id_movie
            movie_showtime.screening_date = form.screening_date.data,
            movie_showtime.time_start = form.time_start.data,
            movie_showtime.seats = form.seats.data
            db.session.commit()
            flash('Cập nhật lịch chiếu phim thành công!')
            return redirect(url_for('management_movie_showtimes'))
        return render_template('Movie_Showtimes/update.html', form=form, cinemas=cinemas, movies=movies, title="Cập nhật lịch chiếu phim")


@app.route('/management/movie_showtimes/delete/<int:id_movie_showtime>',  methods=['GET', 'POST'])
@login_required
def delete_movie_showtime(id_movie_showtime):
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        movie_showtime = Movie_showtime.query.get(id_movie_showtime)
        db.session.delete(movie_showtime)
        db.session.commit()
        flash('Xóa lịch chiếu phim thành công')
        return redirect(url_for('management_movie_showtimes'))


@app.route('/management')
@login_required
def admin():
    if current_user.is_admin == False:
        flash('Bạn không có quyền truy cập vào trang web này!')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('management_users'))
