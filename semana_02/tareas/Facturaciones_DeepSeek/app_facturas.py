# app_facturas.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = 'clave_secreta_facturas'

# Almacenamiento temporal (en producción usarías una base de datos)
facturas = []
productos_temp = []
contador_facturas = 1

@app.route('/')
def index():
    """Página principal con el formulario para agregar productos"""
    return render_template('index.html', 
                         productos=productos_temp,
                         total=calcular_total())

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    """Agrega un producto a la factura temporal"""
    try:
        producto = request.form['prod']
        precio = float(request.form['precio'])
        unidades = int(request.form['unidades'])
        
        if precio < 0 or unidades < 1:
            flash('Por favor ingresa valores válidos (precio positivo y cantidad mayor a 0)', 'error')
            return redirect(url_for('index'))
        
        # Calcular total del producto
        total_producto = precio * unidades
        
        # Agregar producto a la lista temporal
        productos_temp.append({
            'id': len(productos_temp) + 1,
            'nombre': producto,
            'precio': precio,
            'unidades': unidades,
            'total': total_producto
        })
        
        flash('Producto agregado correctamente', 'success')
        
    except ValueError:
        flash('Por favor ingresa valores numéricos válidos', 'error')
    except Exception as e:
        flash(f'Error al agregar producto: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/eliminar_producto/<int:producto_id>')
def eliminar_producto(producto_id):
    """Elimina un producto de la factura temporal"""
    global productos_temp
    productos_temp = [p for p in productos_temp if p['id'] != producto_id]
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/limpiar_todo')
def limpiar_todo():
    """Limpia todos los productos de la factura temporal"""
    global productos_temp
    productos_temp.clear()
    flash('Todos los productos han sido eliminados', 'success')
    return redirect(url_for('index'))

@app.route('/generar_factura')
def generar_factura():
    """Genera una nueva factura con los productos actuales"""
    global productos_temp, contador_facturas, facturas
    
    if not productos_temp:
        flash('No hay productos para generar la factura', 'error')
        return redirect(url_for('index'))
    
    # Calcular totales
    subtotal = sum(p['total'] for p in productos_temp)
    iva = subtotal * 0.16  # 16% de IVA
    total = subtotal + iva
    
    # Crear factura
    factura = {
        'id': contador_facturas,
        'numero': f"F-{datetime.now().year}-{str(contador_facturas).zfill(3)}",
        'fecha': datetime.now().strftime('%d/%m/%Y'),
        'vencimiento': (datetime.now().replace(day=datetime.now().day + 14)).strftime('%d/%m/%Y'),
        'productos': productos_temp.copy(),
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'cliente': 'Cliente General',
        'fecha_creacion': datetime.now().isoformat()
    }
    
    # Agregar a la lista de facturas
    facturas.append(factura)
    
    # Incrementar contador y limpiar productos temporales
    contador_facturas += 1
    productos_temp.clear()
    
    flash(f'Factura {factura["numero"]} generada correctamente', 'success')
    return redirect(url_for('ver_factura', factura_id=factura['id']))

@app.route('/factura/<int:factura_id>')
def ver_factura(factura_id):
    """Muestra una factura específica"""
    factura = next((f for f in facturas if f['id'] == factura_id), None)
    
    if not factura:
        flash('Factura no encontrada', 'error')
        return redirect(url_for('index'))
    
    return render_template('factura.html', factura=factura)

@app.route('/lista_facturas')
def lista_facturas():
    """Muestra la lista de todas las facturas generadas"""
    return render_template('lista_facturas.html', facturas=facturas)

@app.route('/exportar_factura/<int:factura_id>')
def exportar_factura(factura_id):
    """Exporta una factura en formato JSON (podrías extender esto para PDF)"""
    factura = next((f for f in facturas if f['id'] == factura_id), None)
    
    if not factura:
        flash('Factura no encontrada', 'error')
        return redirect(url_for('index'))
    
    # Crear archivo JSON temporal
    filename = f"factura_{factura['numero']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(factura, f, ensure_ascii=False, indent=2)
    
    return send_file(filename, as_attachment=True, download_name=filename)

# Funciones auxiliares
def calcular_total():
    """Calcula el total de los productos temporales"""
    if not productos_temp:
        return 0
    
    subtotal = sum(p['total'] for p in productos_temp)
    iva = subtotal * 0.16
    return subtotal + iva

def formatear_moneda(valor):
    """Formatea un valor como moneda"""
    return f"${valor:,.2f}"

# Registrar filtro en Jinja2
@app.template_filter('moneda')
def filtro_moneda(valor):
    return formatear_moneda(valor)

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)