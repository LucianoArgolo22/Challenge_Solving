with operaciones_rankeadas as(
			select 
				fecha, desc_marca,
				costo, venta,
				(venta - costo) as ganancia_neta,
				ROW_NUMBER () over (partition by desc_marca order by fecha, desc_marca) as primeras_operaciones
			from movimientos 
),
primeras_operaciones_perdida as (
	select fecha, desc_marca, ganancia_neta, primeras_operaciones 
	from operaciones_rankeadas
	where (primeras_operaciones <= 3 and ganancia_neta < 0)
),
primera_operacion_ganancia as (
	select fecha, desc_marca, ganancia_neta, primeras_operaciones 
	from operaciones_rankeadas
	where (primeras_operaciones = 4 and ganancia_neta > 0)
)
select fecha, desc_marca, (venta - costo) as ganancia_neta, primeras_operaciones  from operaciones_rankeadas
where desc_marca in
				(select distinct(desc_marca) from primeras_operaciones_perdida)
and desc_marca in (select distinct(desc_marca) from primera_operacion_ganancia)
order by desc_marca, fecha;