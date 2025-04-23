# app1.py

from flask import Flask, jsonify, request
from datos import books
from decoradores import medir_tiempo, require_apikey

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>API de libros</h1><p>Consulta libros por ID, título o listado completo.</p>"

@app.route('/api/v1/book/all', methods=['GET'])
@medir_tiempo
def get_all_books():
    return jsonify(books)

@app.route('/api/v1/book', methods=['GET'])
@medir_tiempo
@require_apikey
def get_book_by_id():
    if 'id' in request.args:
        try:
            book_id = int(request.args['id'])
        except ValueError:
            return jsonify({'error': 'ID debe ser un número'}), 400

        resultado = [book for book in books if book['id'] == book_id]
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'error': 'Libro no encontrado'}), 404
    else:
        return jsonify({'error': 'Falta el parámetro ID'}), 400

@app.route('/api/v1/book', methods=['POST'])
@require_apikey
def add_book():
    data = request.get_json()
    required_fields = ['id', 'title', 'author', 'first_sentence', 'published']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos en la petición'}), 400

    if any(book['id'] == data['id'] for book in books):
        return jsonify({'error': 'Ya existe un libro con ese ID'}), 409

    books.append(data)
    return jsonify({'mensaje': 'Libro añadido correctamente', 'libro': data}), 201

@app.route('/api/v1/book/<int:book_id>', methods=['PUT'])
@require_apikey
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book['id'] == book_id:
            book.update(data)
            return jsonify({'mensaje': 'Libro actualizado', 'libro': book}), 200

    return jsonify({'error': 'Libro no encontrado'}), 404

@app.route('/api/v1/book/<int:book_id>', methods=['DELETE'])
@require_apikey
def delete_book(book_id):
    global books
    original_len = len(books)
    books = [book for book in books if book['id'] != book_id]

    if len(books) == original_len:
        return jsonify({'error': 'Libro no encontrado'}), 404

    return jsonify({'mensaje': f'Libro con id {book_id} eliminado'}), 200

if __name__ == '__main__':
    app.run()