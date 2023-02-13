select *, (venta - costo) as ganancia_neta from (
		select 
			fecha, desc_cli,
			costo, venta
		from movimientos 
				) a
order by fecha, desc_cli
limit 3;