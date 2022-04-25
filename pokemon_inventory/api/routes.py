from flask import Blueprint, request, jsonify
from pokemon_inventory.helpers import token_required
from pokemon_inventory.models import db, User, Species, species_schema, speciess_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required 
def getdata(current_user_token):
    return { 'some': 'value'}

# create Species endpoint
@api.route('/speciess', methods = ['POST'])
@token_required
def create_species(current_user_token):
    name = request.json['name']
    national_dex_number = request.json['national_dex_number']
    generation = request.json['generation']
    types = request.json['types']
    abilities = request.json['abilities']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    species = Species(name, national_dex_number, generation, types, abilities, user_token = user_token)

    db.session.add(species)
    db.session.commit()

    response = species_schema.dump(species)
    return jsonify(response)

# retrieve all Species endpoint
@api.route('/speciess', methods = ['GET'])
@token_required
def get_speciess(current_user_token):
    owner = current_user_token.token
    speciess = Species.query.filter_by(user_token = owner).all()
    response = speciess_schema.dump(speciess)
    return jsonify(response)

# retrieve one Species endpoint
@api.route('/speciess/<id>', methods = ['GET'])
@token_required
def get_species(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        species = Species.query.get(id)
        response = species_schema.dump(species)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# update Species endpoint
@api.route('/speciess/<id>', methods = ['POST', 'PUT'])
@token_required
def update_species(current_user_token, id):
    species = Species.query.get(id) # grab Species instance

    species.name = Species.json['name']   
    species.national_dex_number = request.json['national_dex_number']
    species.generation = request.json['generation']
    species.types = request.json['types']
    species.abilities = request.json['abilities']
    species.user_token = current_user_token.token

    db.session.commit()
    response = species_schema.dump(species)
    return jsonify(response)

# delete Species endpoint
@api.route('/speciess/<id>', methods = ['DELETE'])
@token_required
def delete_species(current_user_token, id):
    species = Species.query.get(id)
    db.session.delete(species)
    db.session.commit()
    response = species_schema.dump(species)
    return jsonify(response)