"""CRUD operations"""

from model import db, User, Building, Complaint, Violation, Review, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Returns a user by their user id"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Returns a user by their email"""

    return User.query.filter(User.email == email).first()


def create_building(street_number, street_name, street_suffix, zip_code, lat_long=None): 
    """Create and return a new building"""

    building = Building(street_number=street_number, 
    street_name=street_name, street_suffix=street_suffix, zip_code=zip_code, 
    lat_long=lat_long)

    db.session.add(building)
    db.session.commit()

    return building
    

def get_buildings():
    """Return all buildings"""

    return Building.query.all()


def get_building_by_id(building_id):
    """Returns a building by its building_id"""

    return Building.query.options(db.joinedload('complaints'))\
                        .options(db.joinedload('violations'))\
                        .options(db.joinedload('reviews'))\
                        .get(building_id)

                
def get_building_by_address(street_number, street_name, street_suffix, zip_code):
    """Returns a building by its street address"""

    return Building.query.options(db.joinedload('complaints'))\
                        .options(db.joinedload('violations'))\
                        .options(db.joinedload('reviews')) \
                        .filter_by(street_number=street_number). \
                        filter_by(street_name=street_name). \
                        filter_by(street_suffix=street_suffix). \
                        filter_by(zip_code=zip_code).first()


def create_complaint(complaint_number, building_id, complaint_description, date_filed):
    """Create and return a new complaint"""

    complaint = Complaint(complaint_number=complaint_number, 
                        building_id=building_id, 
                        complaint_description=complaint_description, 
                        date_filed=date_filed)

    db.session.add(complaint)
    db.session.commit()

    return complaint


def get_complaint(complaint_number):
    """Get a complaint"""

    return Complaint.query.get(complaint_number)


def create_violation(complaint_number, building_id, nov_category_description, item, nov_item_description, date_filed):
    """Create and return a new violation"""

    violation = Violation(complaint_number=complaint_number, 
                        building_id=building_id, 
                        nov_category_description=nov_category_description,
                        item = item,
                        nov_item_description = nov_item_description, 
                        date_filed=date_filed)

    db.session.add(violation)
    db.session.commit()

    return violation


def create_review(building_id, user_id, review_date, review_text, rating=None, landlord_name=None):
    """Create and return a new review."""

    review = Review(building_id=building_id, 
                    user_id=user_id, review_date=review_date, 
                    review_text=review_text, rating=rating, 
                    landlord_name=landlord_name)

    db.session.add(review)
    db.session.commit()

    return review


def get_reviews():
    """Return all reviews"""

    return Review.query.all()


def get_review_by_id(building_id): 
    """Returns a review by its review id"""

    return Review.query.options(db.joinedload('users')).filter_by(building_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)