#tabla a crear para que la información sea insertada
create table challenge.movimientos(
Fecha Date,
Descripcion_Cliente varchar(200),
Descripcion_Proveedor varchar(200),
Descripcion_Producto varchar(200),
Descripcion_Marca varchar(200),
Cantidad int,
Costo float,
Venta float,
Ganancia_Neta float
);


#información a insertar en la tabla con los joins
with prod as (
	select 
		p.cod_prod, p.cod_marca, p.cod_proveedor,
		m.descripcion as desc_marca,
		prov.descripcion as desc_prov, p.descripcion as desc_prod
	from challenge.Data_productos p
		inner join challenge.Data_Marcas m
			on p.Cod_Marca = m.Cod_Marca
		inner join challenge.Data_Proveedores prov
			on prov.Cod_proveedor = p.Cod_proveedor
),
movimientos_prod as (
	select p.*,
		mov.cod_cliente, mov.fecha, mov.cantidad, mov.costo, mov.venta
	from prod p
		inner join challenge.Data_Movimientos mov
			on p.cod_prod = mov.cod_prod
),
movimientos_cli as (
	select mp.*,
		cli.cod_cliente as cod_cliente2, cli.descripcion as desc_cli
	from movimientos_prod mp
		inner join 	challenge.Data_Clientes as cli
			on cli.cod_cliente = mp.cod_cliente
),
movimientos as (
	select 
	fecha, desc_cli, desc_prov, desc_prod, desc_marca, cantidad, costo, venta
	from movimientos_cli 
)
select * from movimientos;
