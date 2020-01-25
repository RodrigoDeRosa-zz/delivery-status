from src.status_service import StatusService


def main():
    notifications = [
        {
            'status': 'delivered'
        },
        {
            'status': 'not delivered',
            'substatus': 'stolen'
        },
        {
            'status': 'handling'
        },
        {
            'status': 'shipped'
        },
        {
            'status': 'handling',
            'substatus': 'manufacturing'
        }
    ]
    print(StatusService.package_status(notifications))


if __name__ == '__main__':
    main()
