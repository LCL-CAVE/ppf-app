import dash_mantine_components as dmc


def create_btn_run(label, id, variant):
    return dmc.Button(
        label,
        id=id,
        variant=variant,
        fullWidth=True,
    )
