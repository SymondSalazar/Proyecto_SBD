-- ========================================
-- INSERCIÓN DE DATOS REALISTAS
-- ========================================

-- 1. Cuentas (usuarios base)
INSERT INTO cuentas (id, email, nombre, fecha_creacion, contrasena) VALUES
('USR001', 'ana.torres@mail.com', 'Ana Torres', '2023-01-15', 'PassAna#23'),
('USR002', 'carlos.mendez@corp.com', 'Carlos Méndez', '2023-02-20', 'Secure789!'),
('USR003', 'lucia.garcia@shop.com', 'Lucía García', '2023-03-10', 'Lg2023*'),
('USR004', 'pedro.vargas@biz.com', 'Pedro Vargas', '2023-04-05', 'P3dr0V!'),
('USR005', 'marta.lopez@mail.com', 'Marta López', '2023-05-18', 'M@rt4Secure'),
('USR006', 'juan.rojas@corp.com', 'Juan Rojas', '2023-06-22', 'RojasJ2023$'),
('USR007', 'sofia.castro@biz.com', 'Sofía Castro', '2023-07-30', 'SofiC!789'),
('USR008', 'diego.ramos@mail.com', 'Diego Ramos', '2023-08-14', 'D1eg0R@'),
('USR009', 'elena.miranda@shop.com', 'Elena Miranda', '2023-09-05', '3l3n@M!'),
('USR010', 'oscar.duarte@corp.com', 'Oscar Duarte', '2023-10-19', '0sc@rD#');

-- 2. Clientes
INSERT INTO clientes (cuenta_id, direccion_envio, metodo_pago) VALUES
('USR001', 'Calle Primavera 234, Col. Centro, CDMX, CP 06000', 'TARJETA'),
('USR002', 'Av. Universidad 567, Col. Del Valle, Monterrey, CP 66220', 'PAYPAL'),
('USR003', 'Paseo Reforma 890, Col. Juárez, Guadalajara, CP 44100', 'TARJETA'),
('USR005', 'Callejón del Beso 12, Col. Centro, Guanajuato, CP 36000', 'PAYPAL'),
('USR006', 'Blvd. Díaz Ordaz 345, Col. Olímpica, Tijuana, CP 22330', 'TARJETA'),
('USR008', 'Av. Insurgentes 678, Col. Roma, CDMX, CP 06700', 'PAYPAL'),
('USR010', 'Callejón San Francisco 45, Col. Centro, Puebla, CP 72000', 'TARJETA');

-- 3. Vendedores
-- Se cambian las valoraciones antiguas (ALTA/MEDIA/BAJA) por valores numéricos (estrellas)
-- Mapeo asumido: ALTA -> 5.0, MEDIA -> 3.0, BAJA -> 1.0
INSERT INTO vendedores (cuenta_id, descripcion, valoracion) VALUES
('USR004', 'Electrónicos premium con garantía extendida', 5.0),
('USR005', 'Moda sostenible y productos ecológicos', 3.0),
('USR007', 'Libros especializados y coleccionables', 5.0),
('USR009', 'Arte y decoración artesanal mexicana', 1.0),
('USR010', 'Deportes y actividades al aire libre', 3.0);

---"juguetes", "ropa", "tecnologia", "hogar"
-- 4. Productos
INSERT INTO productos (id, nombre, descripcion, calificacion, stock, precio, categoria, vendedor_id) VALUES
('PROD1001', 'Smartphone X9', '6.5" AMOLED, 128GB RAM, Triple Cámara', 4.5, 50, 8999.99, 'ELECTRONICA', 'USR004'),
('PROD1002', 'Zapatos Running Air', 'Material transpirable, tallas 22-30', 4.2, 120, 1299.50, 'CALZADO', 'USR005'),
('PROD1003', 'Cien Años de Soledad', 'Edición especial aniversario', 4.8, 80, 450.00, 'LIBROS', 'USR007'),
('PROD1004', 'Pulsera Artesanal Plata', 'Hecha a mano por artesanos oaxaqueños', 3.9, 35, 799.00, 'JOYERIA', 'USR009'),
('PROD1005', 'Router WiFi 6', 'Doble banda, 3000Mbps, 8 antenas', 4.1, 40, 2399.00, 'ELECTRONICA', 'USR004'),
('PROD1006', 'Set Yoga Premium', 'Incluye mat, bloques y correa', 4.3, 90, 899.00, 'DEPORTES', 'USR010'),
('PROD1007', 'Cámara DSLR 24MP', 'Grabación 4K, kit 2 lentes', 4.7, 25, 15499.00, 'FOTOGRAFIA', 'USR004'),
('PROD1008', 'Vestido Lino Verano', 'Tallas S-XL, 4 colores disponibles', 4.0, 70, 899.00, 'ROPA', 'USR005'),
('PROD1009', 'El Principito Ed. Tapa Dura', 'Ilustraciones originales', 4.9, 110, 350.00, 'LIBROS', 'USR007'),
('PROD1010', 'Mochila Excursionismo', '40L, impermeable, soporte 15kg', 4.4, 60, 2199.00, 'DEPORTES', 'USR010'),
('PROD1011', 'Aceite Esencial Lavanda', '100% puro, 30ml', 3.8, 200, 299.00, 'BELLEZA', 'USR009'),
('PROD1012', 'Teclado Mecánico RGB', 'Switches Blue, retroiluminado', 4.2, 45, 1399.00, 'ELECTRONICA', 'USR004'),
('PROD1013', 'Set Café Artesanal', '4 variedades de Chiapas, 250g cada una', 4.6, 85, 599.00, 'ALIMENTOS', 'USR005'),
('PROD1014', 'Balón Fútbol Profesional', 'Tamaño 5, material sintético', 4.3, 150, 899.00, 'DEPORTES', 'USR010'),
('PROD1015', 'Lámpara Sal del Himalaya', 'Base de madera, 20cm altura', 3.7, 40, 650.00, 'HOGAR', 'USR009');

-- 5. Pedidos
INSERT INTO pedidos (id, cliente_id, direccion_entrega, fecha_entrega, fecha_compra, estado_envio) VALUES
('PED10001', 'USR001', 'Calle Primavera 234, Col. Centro, CDMX, CP 06000', '2023-05-20', '2023-05-15', 'ENTREGADO'),
('PED10002', 'USR002', 'Av. Universidad 567, Col. Del Valle, Monterrey, CP 66220', '2023-06-10', '2023-06-01', 'ENTREGADO'),
('PED10003', 'USR003', 'Paseo Reforma 890, Col. Juárez, Guadalajara, CP 44100', '2023-07-05', '2023-06-28', 'ENTREGADO'),
('PED10004', 'USR005', 'Callejón del Beso 12, Col. Centro, Guanajuato, CP 36000', '2023-08-12', '2023-08-10', 'ENTREGADO'),
('PED10005', 'USR006', 'Blvd. Díaz Ordaz 345, Col. Olímpica, Tijuana, CP 22330', '2023-09-01', '2023-08-25', 'ENVIADO'),
('PED10006', 'USR001', 'Calle Primavera 234, Col. Centro, CDMX, CP 06000', '2023-10-15', '2023-10-10', 'EN_PROCESO'),
('PED10007', 'USR008', 'Av. Insurgentes 678, Col. Roma, CDMX, CP 06700', '2023-11-20', '2023-11-15', 'ENVIADO'),
('PED10008', 'USR002', 'Av. Universidad 567, Col. Del Valle, Monterrey, CP 66220', '2023-12-05', '2023-11-30', 'ENTREGADO'),
('PED10009', 'USR010', 'Callejón San Francisco 45, Col. Centro, Puebla, CP 72000', '2024-01-10', '2024-01-02', 'ENTREGADO'),
('PED10010', 'USR003', 'Paseo Reforma 890, Col. Juárez, Guadalajara, CP 44100', '2024-02-15', '2024-02-10', 'EN_PROCESO'),
('PED10011', 'USR005', 'Callejón del Beso 12, Col. Centro, Guanajuato, CP 36000', '2024-03-18', '2024-03-12', 'ENVIADO'),
('PED10012', 'USR006', 'Blvd. Díaz Ordaz 345, Col. Olímpica, Tijuana, CP 22330', '2024-04-22', '2024-04-15', 'ENTREGADO'),
('PED10013', 'USR008', 'Av. Insurgentes 678, Col. Roma, CDMX, CP 06700', NULL, '2024-05-10', 'EN_CARRITO'),
('PED10014', 'USR010', 'Callejón San Francisco 45, Col. Centro, Puebla, CP 72000', NULL, '2024-05-12', 'EN_CARRITO'),
('PED10015', 'USR001', 'Calle Primavera 234, Col. Centro, CDMX, CP 06000', '2024-05-20', '2024-05-15', 'ENTREGADO');

-- 6. Pedidos_Productos (Detalles de compra)
INSERT INTO pedidos_productos (pedido_id, producto_id, cantidad) VALUES
('PED10001', 'PROD1001', 1),
('PED10001', 'PROD1005', 2),
('PED10002', 'PROD1003', 3),
('PED10003', 'PROD1002', 1),
('PED10004', 'PROD1006', 1),
('PED10004', 'PROD1010', 1),
('PED10005', 'PROD1007', 1),
('PED10006', 'PROD1008', 2),
('PED10006', 'PROD1013', 1),
('PED10007', 'PROD1009', 4),
('PED10008', 'PROD1012', 1),
('PED10009', 'PROD1014', 2),
('PED10010', 'PROD1004', 1),
('PED10011', 'PROD1011', 3),
('PED10012', 'PROD1005', 1),
('PED10012', 'PROD1012', 1),
('PED10013', 'PROD1003', 2),
('PED10014', 'PROD1015', 1),
('PED10015', 'PROD1001', 1),
('PED10015', 'PROD1009', 1);

-- 7. Reseñas de productos
INSERT INTO productos_resenas (id, cliente_id, producto_id, calificacion, comentario, fecha_resena) VALUES
('REV001', 'USR001', 'PROD1001', 5, 'Excelente rendimiento y pantalla de alta calidad', '2023-05-25 14:30:00'),
('REV002', 'USR002', 'PROD1003', 4, 'Hermosa edición, pero llegó con una pequeña abolladura', '2023-06-15 10:15:00'),
('REV003', 'USR003', 'PROD1002', 3, 'Cómodos pero se desgastaron rápido', '2023-07-10 16:45:00'),
('REV004', 'USR005', 'PROD1006', 5, 'Perfecto para mis rutinas diarias, muy resistente', '2023-08-20 09:20:00'),
('REV005', 'USR006', 'PROD1007', 5, 'Calidad profesional a precio accesible', '2023-09-05 11:40:00'),
('REV006', 'USR008', 'PROD1009', 4, 'Las ilustraciones son preciosas, papel de alta calidad', '2023-11-25 15:10:00'),
('REV007', 'USR002', 'PROD1012', 3, 'Buen teclado pero el RGB tiene algunas fallas', '2023-12-10 13:25:00'),
('REV008', 'USR010', 'PROD1014', 4, 'Excelente agarre y durabilidad', '2024-01-15 17:30:00'),
('REV009', 'USR005', 'PROD1013', 5, 'Café aromático y de excelente sabor', '2024-03-20 10:50:00'),
('REV010', 'USR001', 'PROD1009', 5, 'Edición de colección, vale cada peso', '2024-05-18 14:15:00');