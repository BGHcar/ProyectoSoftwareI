class ServicioAplicacionTransacciones:
    def __init__(self, repositorio_transacciones, generador_informes):
        self.repositorio_transacciones = repositorio_transacciones
        self.generador_informes = generador_informes

    def realizar_transaccion(self, transaccion):
        # Lógica para realizar una transacción
        self.repositorio_transacciones.guardar(transaccion)
        return "Transacción completada con éxito."

    def generar_informe_financiero(self, fecha_inicio, fecha_fin):
        # Lógica para generar un informe financiero
        transacciones = self.repositorio_transacciones.buscar_por_rango_de_fechas(fecha_inicio, fecha_fin)
        informe = self.generador_informes.generar(transacciones)
        return informe