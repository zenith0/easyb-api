from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Category, Expense, Income, Accounting, engine

Session = sessionmaker(bind=engine)
session = Session()

class CategoryApi:
    def create_category():
        category_name = request.json.get('name')
        with Session() as session:
            category_exists = session.query(Category).filter_by(name=category_name).first()
            if not category_exists:
                new_category = Category(name=category_name)
                session.add(new_category)
                session.commit()
                return jsonify({'message': f'Category "{category_name}" created successfully', 'id': new_category.id, 'name': category_name}), 201
            else:
                return jsonify({'message': f'Category "{category_name}" already exists'}), 400
    
    def get_categories():
        with Session() as session:
            categories = session.query(Category).all()
            categories_data = [{'id': category.id, 'name': category.name} for category in categories]
            return jsonify({'categories': categories_data})


    def get_categories_with_items():
        categories = []
        with Session() as session:
            categories = session.query(Category).all()
            categories_with_items = []
            for category in categories:
                acc_items_in_category = session.query(Accounting).filter_by(category_id=category.id).all()
                exp_items_in_category = session.query(Expense).filter_by(category_id=category.id).all()
                inc_items_in_category = session.query(Income).filter_by(category_id=category.id).all()
                
                categories_with_items.append({"id": category.id,
                                            "name": category.name,
                                            "acc_items": [item.id for item in acc_items_in_category],
                                            "exp_items": [item.id for item in exp_items_in_category],
                                            "inc_items": [item.id for item in inc_items_in_category]})

            return jsonify(categories_with_items)
    
    def update_category():
        category_id = request.json.get('id')
        new_category_name = request.json.get('name')
        with Session() as session:
            category = session.query(Category).filter_by(id=category_id).first()
            if category:
                category.name = new_category_name
                session.commit()
                return jsonify({'message': f'Category updated successfully'}), 200
            else:
                return jsonify({'message': f'Category with ID "{category_id}" not found'}), 404

    def delete_category():
        category_id = request.json.get('id')
        with Session() as session:
            category = session.query(Category).filter_by(id=category_id).first()
            if category:
                # Set associated accounting items' category_id to null
                session.query(Accounting).filter_by(category_id=category_id).update({Accounting.category_id: None})
                # Delete the category
                session.delete(category)
                session.commit()
                return jsonify({'message': f'Category deleted successfully'}), 200
            else:
                return jsonify({'message': f'Category with ID "{category_id}" not found'}), 404
