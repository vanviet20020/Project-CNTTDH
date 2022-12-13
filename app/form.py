from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    RadioField,
    EmailField,
    HiddenField,
    DateField
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    EqualTo,
)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import User, Supplier
from sqlalchemy import and_


class SignUpUser(FlaskForm):
    fullname = StringField('Họ tên', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField(
        'Mật khẩu',
        validators=[
            DataRequired(),
            Length(min=6, message=('Mật khẩu quá ngắn! Nhập tối thiểu 6 kí tự')),
        ],
    )
    rePassword = PasswordField(
        'Nhập lại mật khẩu',
        validators=[
            DataRequired(),
            EqualTo('password', message='Mật khẩu không trùng!'),
        ])
    phone_number = StringField(
        'Số điện thoại',
        validators=[
            DataRequired(),
            Length(min=10, max=10, message=(
                'Số điện thoại bạn nhập không tồn tại!')),
        ],
    )
    gender = RadioField(
        'Giới tính',
        choices=['Nam', 'Nữ', 'Khác'],
        validators=[DataRequired()],
    )
    submit = SubmitField('Đăng ký')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(
                'Email đã được xử dụng! Hãy sử dụng email khác.')

    def validate_phone(self, phone_number):
        phone_number = User.query.filter_by(
            phone_number=phone_number.data).first()
        if phone_number is not None:
            raise ValidationError(
                'Số điện thoại đã được xử dụng! Hãy sử dụng Số điện thoại khác.'
            )


class UpdateUser(FlaskForm):
    id_user = HiddenField(validators=[DataRequired()])
    fullname = StringField('Họ tên', validators=[DataRequired()])
    phone_number = StringField(
        'Số điện thoại',
        validators=[
            DataRequired(),
            Length(min=10, max=10, message=(
                'Số điện thoại bạn nhập không tồn tại.')),
        ],
    )
    gender = RadioField(
        'Giới tính',
        choices=['Nam', 'Nữ', 'Khác'],
        validators=[DataRequired()],
    )
    is_admin = RadioField('Quản trị viên', choices=['Có', 'Không'])
    submit = SubmitField('Cập nhật')

    def validate_phone(self, phone_number, id_user):
        phone_number = User.query.filter(
            and_(User.id != id_user.data, User.phone_number == phone_number.data)).first()
        if phone_number is not None:
            raise ValidationError(
                'Số điện thoại đã được xử dụng! Hãy sử dụng Số điện thoại khác.'
            )


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Nhớ tài khoản')
    submit = SubmitField('Đăng nhập')


class SupplierForm(FlaskForm):
    name = StringField('Tên nhà cung cấp', validators=[DataRequired()])
    photo = FileField('Ảnh giá vé', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Xong')


class CinemaForm(FlaskForm):
    name = StringField('Tên rạp chiếu phim', validators=[DataRequired()])
    address = StringField('Địa chỉ', validators=[DataRequired()])
    district = StringField('Quận/Huyện', validators=[DataRequired()])
    hotline = StringField('Hotline')
    lng = StringField('Kinh độ', validators=[DataRequired()])
    lat = StringField('Vĩ độ', validators=[DataRequired()])
    submit = SubmitField('Xong')


class MovieForm(FlaskForm):
    name = StringField('Tên phim', validators=[DataRequired()])
    photo = FileField('Ảnh phim', validators=[FileRequired()])
    describe = StringField('Mô tả')
    director = StringField('Đạo diễn')
    actor = StringField('Diễn viên')
    genre = StringField('Thể loại')
    release_date = StringField('Ngày công chiếu', validators=[DataRequired()])
    running_time = StringField('Thời gian chiếu', validators=[DataRequired()])
    language = StringField('Ngôn ngữ')
    rated = StringField('Khuyến cáo')
    submit = SubmitField('Xong')


class MovieShowtimeForm(FlaskForm):
    screening_date = DateField('Ngày chiếu', validators=[DataRequired()])
    time_start = StringField('Giờ chiếu')
    seats = StringField('Số ghế ngồi')
    submit = SubmitField('Xong')
