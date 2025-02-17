from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from contactanos.models import Contacto
from solicitudes.models import Registration
from .models import Seccion, Tarifa, CuentaPorCobrar, Factura
from secciones.models import  SeccionEstudiante
from django.db.models import Sum
from .serializers import CuentaPorCobrarSerializer
from estudiantes.models import Estudiante
from dateutil.relativedelta import relativedelta
from datetime import date, timezone
from .serializers import TarifaSerializer, CuentaPorCobrarSerializer, FacturaSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view
from django.http import JsonResponse

from profesores.models import  Profesor
from rest_framework.decorators import api_view

# API para listar y crear tarifas
class TarifaListCreateAPI(generics.ListCreateAPIView):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API para actualizar y eliminar tarifas
class TarifaDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer

# API para listar cuentas por cobrar
class CuentaPorCobrarListAPI(generics.ListAPIView):
    queryset = CuentaPorCobrar.objects.all()
    serializer_class = CuentaPorCobrarSerializer



from decimal import Decimal, ROUND_DOWN
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone

@api_view(['POST'])
def generar_cuentas_api(request):
    mensajes_exito = []
    mensajes_error = []

    try:
        with transaction.atomic():  # Asegura que todas las operaciones se realicen en una sola transacción
            secciones = Seccion.objects.all()  # Obtener todas las secciones, no solo las terminadas

            if not secciones:
                return Response({"warning": "No hay secciones para generar facturas."}, status=status.HTTP_400_BAD_REQUEST)

            for seccion in secciones:
                seccion_estudiantes = SeccionEstudiante.objects.filter(seccion=seccion)
                estudiantes = [inscripcion.estudiante for inscripcion in seccion_estudiantes]

                if not estudiantes:
                    mensajes_error.append(f"No hay estudiantes en la sección {seccion.id}.")
                    continue

                try:
                    tarifa = Tarifa.objects.get(secciones_tarifa=seccion)
                except Tarifa.DoesNotExist:
                    mensajes_error.append(f"No se encontró tarifa para la sección {seccion.id}.")
                    continue

                # Calcular la duración en meses de la sección
                delta_dias = (seccion.fecha_termino - seccion.fecha_inicio).days
                meses_duracion = delta_dias / 30  # Dividir entre 30 para obtener meses aproximados
                meses_duracion = round(meses_duracion)  # Redondeamos al mes más cercano

                if meses_duracion <= 0:
                    mensajes_error.append(f"La duración de la sección {seccion.id} es inválida (menos de un mes).")
                    continue

                monto_total = Decimal(tarifa.precio)
                monto_por_mes = monto_total / meses_duracion

                # Redondear el monto por mes a 2 decimales
                monto_por_mes = monto_por_mes.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

                # Asegurarse de que la suma total no exceda el monto total
                total_calculado = monto_por_mes * meses_duracion
                diferencia = monto_total - total_calculado
                if diferencia > 0:
                    # Si hay diferencia debido al redondeo, añadirla al último mes
                    monto_por_mes_ultimo = monto_por_mes + diferencia

                for estudiante in estudiantes:
                    cuenta_existente = CuentaPorCobrar.objects.filter(estudiante=estudiante, seccion=seccion).exists()

                    if not cuenta_existente:
                        fecha_actual = seccion.fecha_inicio
                        for i in range(meses_duracion):
                            # Crear cuenta por cobrar
                            cuenta_por_cobrar = CuentaPorCobrar(
                                estudiante=estudiante,
                                seccion=seccion,
                                fecha_factura=fecha_actual + relativedelta(months=1),
                                monto=monto_por_mes,
                                mes_correspondiente=fecha_actual.month,
                                estado='pendiente'
                            )
                            cuenta_por_cobrar.save()
                            mensajes_exito.append(f"Cuenta creada para estudiante: {estudiante.id} en sección: {seccion.id}.")

                            # Crear factura asociada
                            nueva_factura = Factura(
                                estudiante=estudiante,
                                cuenta_por_cobrar=cuenta_por_cobrar,
                                mes_correspondiente=fecha_actual.month,
                                fecha_emision=timezone.now(),
                                total=monto_por_mes,
                                pagado=False
                            )
                            nueva_factura.save()
                            mensajes_exito.append(f"Factura creada para estudiante: {estudiante.id} en sección: {seccion.id}.")

                            # Incrementar un mes
                            fecha_actual += relativedelta(months=1)

                        # Si hay diferencia en el último mes, corregirlo
                        if diferencia > 0:
                            cuenta_por_cobrar_ultimo = CuentaPorCobrar.objects.filter(estudiante=estudiante, seccion=seccion, mes_correspondiente=fecha_actual.month).first()
                            cuenta_por_cobrar_ultimo.monto = monto_por_mes_ultimo
                            cuenta_por_cobrar_ultimo.save()

                            # También la factura
                            factura_ultimo = Factura.objects.filter(cuenta_por_cobrar=cuenta_por_cobrar_ultimo).first()
                            factura_ultimo.total = monto_por_mes_ultimo
                            factura_ultimo.save()
                            mensajes_exito.append(f"Factura ajustada para estudiante: {estudiante.id} en sección: {seccion.id}, último mes.")

        if mensajes_exito:
            return Response({"success": "\n".join(mensajes_exito)}, status=status.HTTP_201_CREATED)
        if mensajes_error:
            return Response({"errors": "\n".join(mensajes_error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"info": "No se generaron cuentas ni facturas. No hay secciones por facturar."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API para pagar factura
@api_view(['POST'])
def pagar_factura_api(request, cuenta_id, factura_id):
    cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
    factura = get_object_or_404(Factura, id=factura_id)

    if factura.pagado:
        return Response({"error": "La factura ya ha sido pagada."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        factura.pagado = True
        factura.save()

        # Marcar la cuenta como pagada si todas las facturas están pagadas
        if not cuenta.facturas.filter(pagado=False).exists():
            cuenta.estado = 'pagado'
            cuenta.save()

    return Response({"success": "Pago registrado."}, status=status.HTTP_200_OK)





@api_view(['GET'])
def obtener_detalle_factura(request, cuenta_id, factura_id):
    # Obtener la cuenta y la factura
    cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
    factura = get_object_or_404(Factura, id=factura_id)

    # Obtener el estudiante asociado a la cuenta (suponiendo que la relación existe)
    estudiante = cuenta.estudiante  # Relación entre CuentaPorCobrar y Estudiante

    # Preparar los datos para enviar en formato JSON
    factura_data = {
        'id': factura.id,
        'numero_factura': factura.numero_factura,
        'total': factura.total,
        'fecha_emision': factura.fecha_emision,
        'pagado': factura.pagado,
        'mes_correspondiente': factura.mes_correspondiente,
    }

    cuenta_data = {
        'id': cuenta.id,
        'estado': cuenta.estado,
        'monto': cuenta.monto,
        'fecha_creacion': cuenta.fecha_creacion,
        'fecha_factura': cuenta.fecha_factura,
        'mes_correspondiente': cuenta.mes_correspondiente,
    }

    estudiante_data = {
        'id': estudiante.id,
        'nombre': estudiante.nombre,
        'apellido': estudiante.apellido,
        'email': estudiante.email,
        # Otros campos relevantes de Estudiante
    }

    # Responder con los datos en formato JSON
    return Response({
        'cuenta': cuenta_data,
        'factura': factura_data,
        'estudiante': estudiante_data,  # Añadimos la información del estudiante
    })


@api_view(['GET'])
def listar_facturas_api(request):
    try:
        # Obtener facturas pagadas y no pagadas
        facturas_pagadas = Factura.objects.filter(pagado=True).select_related('estudiante')
        facturas_no_pagadas = Factura.objects.filter(pagado=False).select_related('estudiante')

        # Serializar datos
        pagadas_serializer = FacturaSerializer(facturas_pagadas, many=True)
        no_pagadas_serializer = FacturaSerializer(facturas_no_pagadas, many=True)

        return Response({
            'facturas_pagadas': pagadas_serializer.data,
            'facturas_no_pagadas': no_pagadas_serializer.data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from django.db import models



@api_view(['GET'])
def resumen_facturas_api(request):
    try:
        # Obtener el monto total de facturas pagadas y no pagadas en una sola consulta
        resumen = Factura.objects.aggregate(
            total_pagado=Sum('total', filter=models.Q(pagado=True)),
            total_no_pagado=Sum('total', filter=models.Q(pagado=False))
        )
          # Contar la cantidad de estudiantes inscritos
        cantidad_estudiantes = Estudiante.objects.count()

        # Contar la cantidad de secciones
        cantidad_secciones = Seccion.objects.count()

            # Contar la cantidad de solicitudes
        cantidad_solicitudes = Registration.objects.count()

        # Contar la cantidad de contactanos
        cantidad_contactanos = Contacto.objects.count()

        # Contar la cantidad de profesores
        cantidad_profesores = Profesor.objects.count()
        # Si no hay registros, el valor de las sumas será None, así que lo asignamos a 0
        total_pagado = resumen['total_pagado'] if resumen['total_pagado'] is not None else 0
        total_no_pagado = resumen['total_no_pagado'] if resumen['total_no_pagado'] is not None else 0

        # Responder con los valores calculados
        return Response({
            'monto_pagado': total_pagado,
            'monto_no_pagado': total_no_pagado,
            'cantidad_estudiantes': cantidad_estudiantes,
            'cantidad_secciones': cantidad_secciones,
            'cantidad_profesores': cantidad_profesores,
            'cantidad_solicitudes': cantidad_solicitudes,  # Agregado
            'cantidad_contactanos': cantidad_contactanos,  # Agregado
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # En caso de error, retornar un mensaje de error genérico
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

