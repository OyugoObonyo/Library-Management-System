"""
A module tasked with creating forms related to the book blueprint
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class AddBookForm(FlaskForm):
    """
    A class that creates a form to add books to the database
    """
    title = StringField('Book title', validators=[DataRequired()])
    synopsis = StringField('Book description', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_of_publish = IntegerField('Year of publishment', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(), FileAllowed('jpg', 'jpeg', 'png')])
    submit = SubmitField('Add book')


class UpdateBookForm(FlaskForm):
    """
    A class that creates a form to update a particular book in the database
    """
    title = StringField('Book title', validators=[DataRequired()])
    synopsis = StringField('Book description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Update book')
