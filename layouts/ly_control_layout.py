from controls.cl_control_accordion import create_control_accordion
from controls.cl_button_run import create_btn_run
import dash_mantine_components as dmc
from dash import html
import os


def create_control_layout():
    return dmc.Stack(
        id="div-control-layout",
        children=[
            create_control_accordion(),
            create_btn_run("Start", "btn_run", "filled"),
            html.Img(
                src=os.path.join(
                    os.path.dirname('./assets/'),
                    'uni-lu-cave-lab_1.png'),
                className="logo-below-control",
            ),
            dmc.Text("DISCLAIMER. The information and results provided by this web application "
                     " are for general informational purposes only. "
                     "All information on the web application is provided in good faith, however"
                     " we make no representation or warranty of any kind, express or implied, "
                     "regarding the accuracy, adequacy, validity, reliability, availability, or completeness "
                     "of any information on the application. UNDER NO CIRCUMSTANCE SHALL WE HAVE ANY LIABILITY "
                     "TO YOU FOR ANY LOSS OR DAMAGE OF ANY KIND INCURRED AS A RESULT OF THE SOFTWARE. ",
                     size="xs",
                     className="disclaimer-below-control",),
        ],
    )
