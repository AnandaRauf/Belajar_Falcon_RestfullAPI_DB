import falcon
from pony.orm import db_session, select
from models import Product
from wsgiref import simple_server
class ProductResource:
    @db_session
    def on_get(self, req, resp):
        products = select(p for p in Product)[:]
        resp.media = [{'id': p.id, 'name': p.name, 'price': p.price, 'description': p.description} for p in products]
        resp.status = falcon.HTTP_200

    @db_session
    def on_post(self, req, resp):
        data = req.media
        product = Product(name=data['name'], price=data['price'], description=data['description'])
        resp.media = {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}
        resp.status = falcon.HTTP_201

    @db_session
    def on_get_single(self, req, resp, product_id):
        product = Product.get(id=product_id)
        if product:
            resp.media = {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {'error': 'Product not found'}
            resp.status = falcon.HTTP_404

    @db_session
    def on_put(self, req, resp, product_id):
        product = Product.get(id=product_id)
        if product:
            data = req.media
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            resp.media = {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {'error': 'Product not found'}
            resp.status = falcon.HTTP_404

    @db_session
    def on_delete(self, req, resp, product_id):
        product = Product.get(id=product_id)
        if product:
            product.delete()
            resp.media = {'message': 'Product deleted'}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {'error': 'Product not found'}
            resp.status = falcon.HTTP_404

app = falcon.App()

product_resource = ProductResource()
app.add_route('/products', product_resource)
app.add_route('/products/{product_id}', product_resource, suffix='single')

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    print("Server running on http://127.0.0.1:8000")
    httpd.serve_forever()