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


-- Trigger: impedir modificaciones a pedidos si su estado actual no está en EN_PROCESO o ENVIADO
DELIMITER $$
CREATE TRIGGER trg_before_update_pedidos
BEFORE UPDATE ON pedidos
FOR EACH ROW
BEGIN
	-- Sólo permitir actualizaciones si el estado previo es EN_PROCESO o ENVIADO
	IF NOT (OLD.estado_envio IN ('EN_PROCESO', 'ENVIADO')) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede modificar el pedido: estado no permite actualizaciones';
	END IF;
END$$
DELIMITER ;


