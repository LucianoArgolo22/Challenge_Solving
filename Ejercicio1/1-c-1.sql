select fecha, desc_marca, ganancia_neta from (
	select 
	*,
	ROW_NUMBER () over (partition by desc_marca order by fecha, desc_marca) as primeras_operaciones
	from (
		select 
			fecha, desc_marca,
			costo, venta,
			(venta - costo) as ganancia_neta
		from movimientos 
				) a
	having ganancia_neta < 0
	)b
where primeras_operaciones <= 3;