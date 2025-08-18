CREATE DATABASE IF NOT EXISTS Proyecto_SBD;
USE Proyecto_SBD;


-- CREACIÓN DE TABLAS

-- Tabla: cuentas 
CREATE TABLE cuentas (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_creacion DATE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    INDEX idx_email (email)
);

-- Tabla: clientes 
CREATE TABLE clientes (
    cuenta_id VARCHAR(10) NOT NULL PRIMARY KEY,
    direccion_envio TEXT NOT NULL,
    metodo_pago ENUM('PAYPAL', 'TARJETA') NOT NULL DEFAULT 'TARJETA',
    FOREIGN KEY (cuenta_id) REFERENCES cuentas(id) 
);

-- Tabla: vendedores 
CREATE TABLE vendedores (
    cuenta_id VARCHAR(10) NOT NULL PRIMARY KEY,
    descripcion TEXT,
    valoracion DECIMAL(2,1) DEFAULT 0.0 CHECK (valoracion >= 0.0 AND valoracion <= 5.0),
    FOREIGN KEY (cuenta_id) REFERENCES cuentas(id) 
);



-- Tabla: productos 
CREATE TABLE productos (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    calificacion DECIMAL(2,1) DEFAULT 0.0 CHECK (calificacion >= 0.0 AND calificacion <= 5.0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    categoria VARCHAR(50) NOT NULL,
    vendedor_id VARCHAR(10) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_categoria (categoria),
    INDEX idx_vendedor (vendedor_id),
    INDEX idx_nombre (nombre),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(cuenta_id) 
);

-- Tabla: pedidos 
CREATE TABLE pedidos (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    cliente_id VARCHAR(10) NOT NULL,
    direccion_entrega TEXT NOT NULL,
    fecha_entrega DATE,
    fecha_compra DATE NOT NULL,
    estado_envio ENUM('EN_CARRITO', 'EN_PROCESO', 'ENVIADO', 'ENTREGADO', 'CANCELADO') 
        NOT NULL DEFAULT 'EN_CARRITO',
    INDEX idx_cliente (cliente_id),
    INDEX idx_estado (estado_envio),
    INDEX idx_fecha_compra (fecha_compra),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cuenta_id) 
);

-- Tabla: pedidos_productos 
CREATE TABLE pedidos_productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id VARCHAR(10) NOT NULL,
    producto_id VARCHAR(10) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    INDEX idx_pedido (pedido_id),
    INDEX idx_producto (producto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ,
    FOREIGN KEY (producto_id) REFERENCES productos(id), 
    UNIQUE KEY unique_pedido_producto (pedido_id, producto_id)
);

-- Tabla: productos_resenas 
CREATE TABLE productos_resenas (
    id VARCHAR(10) NOT NULL PRIMARY KEY,
    cliente_id VARCHAR(10) NOT NULL,
    producto_id VARCHAR(10) NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    fecha_resena TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_producto_resena (producto_id),
    INDEX idx_cliente_resena (cliente_id),
    INDEX idx_calificacion (calificacion),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cuenta_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cliente_producto (cliente_id, producto_id)
);
