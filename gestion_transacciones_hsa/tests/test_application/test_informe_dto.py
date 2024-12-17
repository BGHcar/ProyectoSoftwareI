import unittest
from decimal import Decimal
from application.dtos.informe_dto import InformeDTO

class TestInformeDTO(unittest.TestCase):
    def test_inicializacion_atributos(self):
        # Datos de prueba
        total_depositos = Decimal('1000.0')
        total_retiros = Decimal('500.0')
        saldo_promedio = Decimal('750.0')
        transacciones = []

        # Crear instancia
        informe = InformeDTO(
            total_depositos=total_depositos,
            total_retiros=total_retiros,
            saldo_promedio=saldo_promedio,
            transacciones=transacciones
        )

        # Verificaciones
        self.assertEqual(informe.total_depositos, total_depositos)
        self.assertEqual(informe.total_retiros, total_retiros)
        self.assertEqual(informe.saldo_promedio, saldo_promedio)
        self.assertEqual(informe.transacciones, transacciones)

    def test_repr(self):
        informe = InformeDTO(
            total_depositos=Decimal('1000.0'),
            total_retiros=Decimal('500.0'),
            saldo_promedio=Decimal('750.0'),
            transacciones=[]
        )
        
        esperado = "InformeDTO(total_depositos=1000.0, total_retiros=500.0, saldo_promedio=750.0, transacciones=[])"
        self.assertEqual(repr(informe), esperado)

if __name__ == '__main__':
    unittest.main()
