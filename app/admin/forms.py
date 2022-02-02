"""
A module with forms related to the auth blueprint
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class AddBookForm(FlaskForm):
    """
    A class that creates a form to add books to the database
    """
    title = StringField('Book title', validators=[DataRequired()])
    synopsis = CKEditorField('Book description', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    # Only accept numbers greater than 0
    year_of_publish = IntegerField('Year of publishment', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add book')


class UpdateBookForm(FlaskForm):
    """
    A class that creates a form to update a particular book in the database
    """
    title = StringField('Book title', validators=[DataRequired()])
    synopsis = CKEditorField('Book description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Update book')
