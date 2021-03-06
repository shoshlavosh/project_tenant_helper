"""Models for tenant helper app"""

#import the SQLAlchemy constructor function
from flask_sqlalchemy import SQLAlchemy

#calling the constructor function, creating an instance of 
#SQLAlchemy & assigning it to the variable "db"
db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    #relationship
    reviews = db.relationship("Review", back_populates="user")

    def __repr__(self):
        """Show info about user"""
        return f'<User user_id={self.user_id} email={self.email}>'

    
class Building(db.Model):
    """A building"""

    __tablename__ = 'buildings'

    building_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    street_number = db.Column(db.String) 
    street_name = db.Column(db.String)
    street_suffix = db.Column(db.String, nullable =True)
    zip_code = db.Column(db.String, nullable=True) 
    lat_long = db.Column(db.Integer, nullable=True)

    #relationships
    complaints = db.relationship("Complaint")
    violations = db.relationship("Violation")
    reviews = db.relationship("Review", back_populates="building")


    def __repr__(self):
        """Show info about a building"""
        return f'<Building building_id={self.building_id} \
                    address={self.street_number} {self.street_name} \
                    {self.street_suffix} {self.zip_code}>'
    

class Complaint(db.Model):
    """A building code complaint"""

    __tablename__ = 'complaints'

    complaint_number = db.Column(db.String, 
                            primary_key=True)
    building_id = db.Column(db.Integer, 
                            db.ForeignKey('buildings.building_id'),
                            nullable=True)
    complaint_description = db.Column(db.String, nullable=True)
    date_filed = db.Column(db.DateTime, nullable=True)  
                 
    violations = db.relationship("Violation", uselist=False)

    def __repr__(self):
        """Show a complaint"""
        return f'<Complaint complaint_number={self.complaint_number}, \
                            complaint_description={self.complaint_description}, \
                            date_filed={self.date_filed}>'


class Violation(db.Model):
    """A building code violation"""

    __tablename__ = 'violations'

    violation_id = db.Column(db.Integer, 
                            autoincrement=True,
                            primary_key=True)
    building_id = db.Column(db.Integer, 
                            db.ForeignKey('buildings.building_id'),
                            nullable=True)
    complaint_number = db.Column(db.String, 
                                db.ForeignKey('complaints.complaint_number'), 
                                nullable=True)
    nov_category_description = db.Column(db.String)
    item = db.Column(db.String)
    nov_item_description = db.Column(db.String)
    date_filed = db.Column(db.DateTime) 

    complaints = db.relationship("Complaint", uselist=True, back_populates="violations") 

    def __repr__(self):
        """Show a violation"""
        return f'<Violation complaint_number={self.complaint_number},\
                                        nov_category_description = {self.nov_category_description}, \
                                        item = {self.item}, \
                                        nov_item_description = {self.nov_item_description}, \
                                        date_filed = {self.date_filed}>'


class Review(db.Model):
    """A review of a building / landlord"""

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    building_id = db.Column(db.Integer, 
                            db.ForeignKey('buildings.building_id'))
                            #should be created if there isn't one already
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    review_date = db.Column(db.DateTime) #format '2002, 4, 3' 
                                         #automatically generated
    review_text = db.Column(db.String)
    rating = db.Column(db.Integer, nullable=True) #this is for future implementation
    landlord_name = db.Column(db.String, nullable=True) 

    #relationships
    building = db.relationship("Building", back_populates="reviews") #added back_populates
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        """Show a review"""
        return f'<Review review_date={self.review_date} \
                    user_id={self.user_id} \
                    building_id={self.building_id} \
                    review_text={self.review_text} \
                    landlord_name={self.landlord_name}>'


def connect_to_db(flask_app, db_uri="postgresql:///tenants", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
