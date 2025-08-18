-- Trigger: Para actualizar la calificacion del vendedor automaticamente, luego de crear una reseña
DELIMITER $$
CREATE TRIGGER trg_after_insert_resena
AFTER INSERT ON productos_resenas
FOR EACH ROW
BEGIN
	DECLARE v_vendedor_id VARCHAR(10);
	DECLARE v_promedio DECIMAL(3,2);

	SELECT vendedor_id INTO v_vendedor_id FROM productos WHERE id = NEW.producto_id LIMIT 1;

	IF v_vendedor_id IS NOT NULL THEN
		SELECT AVG(calificacion) INTO v_promedio FROM productos WHERE vendedor_id = v_vendedor_id;

		IF v_promedio IS NULL THEN
			SET v_promedio = 0.0;
		END IF;

		UPDATE vendedores SET valoracion = ROUND(v_promedio, 1) WHERE cuenta_id = v_vendedor_id;
	END IF;
END$$
DELIMITER ;



-- Store Procedure: Modificar estado de pedido según tipo de usuario
DELIMITER $$
CREATE PROCEDURE sp_modificar_pedido(
	IN p_id_pedido VARCHAR(20),
	IN p_nuevo_estado VARCHAR(20),
	IN p_tipo_usuario VARCHAR(10)
)
BEGIN
	DECLARE v_estado_actual VARCHAR(20);

	-- Obtener el estado actual del pedido
	SELECT estado_envio INTO v_estado_actual FROM pedidos WHERE id = p_id_pedido LIMIT 1;

	-- Los permisos del cliente
	IF p_tipo_usuario = 'cliente' THEN

		IF v_estado_actual = 'EN_CARRITO' AND p_nuevo_estado = 'EN_PROCESO' THEN
			UPDATE pedidos SET estado_envio = p_nuevo_estado WHERE id = p_id_pedido;
		ELSE
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El cliente solo puede confirmar el pedido (EN_CARRITO -> EN_PROCESO)';
		END IF;
	
	-- Los permisos del vendedor
	ELSEIF p_tipo_usuario = 'vendedor' THEN
		IF v_estado_actual IN ('EN_PROCESO', 'ENVIADO') THEN
			UPDATE pedidos SET estado_envio = p_nuevo_estado WHERE id = p_id_pedido;
		ELSE
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El vendedor solo puede modificar pedidos en proceso o enviados';
		END IF;
	ELSE
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tipo de usuario no válido';
	END IF;
END$$
DELIMITER ;


