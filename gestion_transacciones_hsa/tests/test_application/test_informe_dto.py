import unittest
from gestion_transacciones_hsa.application.dtos.informe_dto import InformeDTO

class TestInformeDTO(unittest.TestCase):
    def test_inicializacion_atributos(self):
        # Datos de prueba con valores típicos de un informe
        total_depositos = 1000.0  # Monto total de depósitos realizados
        total_retiros = 500.0     # Monto total de retiros efectuados
        saldo_promedio = 750.0    # Promedio del saldo en la cuenta
        transacciones = 10        # Número total de transacciones

        # Crear una nueva instancia de InformeDTO con los datos de prueba
        informe = InformeDTO(
            total_depositos=total_depositos,    # Asigna el total de depósitos
            total_retiros=total_retiros,        # Asigna el total de retiros
            saldo_promedio=saldo_promedio,      # Asigna el saldo promedio
            transacciones=transacciones         # Asigna el número de transacciones
        )

        # Verificaciones para asegurar que los atributos se inicializaron correctamente
        self.assertEqual(informe.total_depositos, total_depositos)  # Verifica el total de depósitos
        self.assertEqual(informe.total_retiros, total_retiros)      # Verifica el total de retiros
        self.assertEqual(informe.saldo_promedio, saldo_promedio)    # Verifica el saldo promedio
        self.assertEqual(informe.transacciones, transacciones)      # Verifica el número de transacciones

    def test_repr(self):
        # Datos de prueba para verificar la representación en cadena
        informe = InformeDTO(
            total_depositos=1000.0,
            total_retiros=500.0,
            saldo_promedio=750.0,
            transacciones=10
        )
        
        # Verifica que la representación en cadena sea correcta
        esperado = "InformeDTO(total_depositos=1000.0, total_retiros=500.0, saldo_promedio=750.0, transacciones=10)"
        self.assertEqual(repr(informe), esperado)

if __name__ == '__main__':
    unittest.main()
