from typing import Iterable

from src.model.package.status import Status


class PackageStatus:

    Handling = Status('Le notificamos al vendedor sobre tu compra', 'Handling')
    Manufacturing = Status('El vendedor tendrá listo tu producto pronto y comenzará el envío', 'Manufacturing')
    ReadyToPrint = Status('El vendedor está preparando tu paquete', 'ReadyToPrint')
    Printed = Status('El vendedor debe despachar tu paquete', 'Printed')
    Shipped = Status('En Camino', 'Shipped')
    SoonDeliver = Status('Pronto a ser entregado', 'SoonDeliver')
    WaitingForWithdrawal = Status('En agencia', 'WaitingForWithdrawal')
    Delivered = Status('Entregado', 'Delivered')
    Lost = Status('Perdido', 'Lost')
    Stolen = Status('Robado', 'Stolen')

    def __dir__(self) -> Iterable[str]:
        result = super(PackageStatus, self).__dir__()
        return [elem for elem in result if '__' not in elem]
