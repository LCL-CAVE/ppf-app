import dash_mantine_components as dmc
from dash import html


def create_notification_progress():
    return dmc.NotificationsProvider(
        [
            html.Div(
                id="notifications-container"
            ),
        ],
        position='top-right',
    )
