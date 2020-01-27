from src.model.package.status import Status


class PackageStatus:

    Handling = Status('Le notificamos al vendedor sobre tu compra')
    Manufacturing = Status('El vendedor tendrá listo tu producto pronto y comenzará el envío')
    ReadyToPrint = Status('El vendedor está preparando tu paquete')
    Printed = Status('El vendedor debe despachar tu paquete')
    Shipped = Status('En Camino')
    SoonDeliver = Status('Pronto a ser entregado')
    WaitingForWithdrawal = Status('En agencia')
    Delivered = Status('Entregado')
    Lost = Status('Perdido')
    Stolen = Status('Robado')
